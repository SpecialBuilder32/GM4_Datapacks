import logging
import os
import sys
from functools import cached_property
from typing import Any, Callable, Optional

from beet import (
    Context,
    InvalidOptions,
    JsonFile,
    ListOption,
    Model,
    PluginOptions
)
from beet.contrib.vanilla import Vanilla
from beet.core.utils import format_validation_error
from mecha import Diagnostic
from pydantic import BaseModel, Extra, ValidationError, validator
from pydantic.error_wrappers import ErrorWrapper

from gm4.utils import add_namespace

CUSTOM_MODEL_PREFIX = 3420000

parent_logger = logging.getLogger("gm4.resource_pack")

# TODO debug loggers ... everywhere

class ModelData(BaseModel):
    """A complete config for a single model"""
    item: ListOption[str]
    reference: str
    model: Optional[str|list[dict[str,Any]]] # defaults to same value as 'reference'
    template: str = "custom"
    textures: Optional[ListOption[str]] # defaults to same value as reference

    @validator('model')
    def default_model(cls, model: str|None, values: dict[str,Any]) -> str|None:
        if model is None and "reference" in values:
            return values["reference"]
        return model
    
    @validator('template')
    def enforce_custom_with_override_predicates(cls, template: str, values: dict[str,Any]) -> str:
        if isinstance(values['model'], list) and template != "custom":
            raise ValidationError([ErrorWrapper(ValueError("specifying complex predicates in 'model' is not compatiable with templating. Option must be 'custom'"), loc=())], model=ModelData)
        return template
    
    @validator('textures')
    def default_texture(cls, textures: ListOption[str], values: dict[str,Any]) -> ListOption[str]:
        if (not textures or not textures.entries()) and isinstance(v:=values.get("reference"), str):
            return ListOption(__root__=[v])
        return textures

    # @validator('template')
    # def template_is_registered(): # TODO is this better than runtime checking?
    #     pass

    # howwever texture validation seems like a good idea to do here, unless that should not be an exception throwing validator
    # @validator("textures")
    # def check_textures_defined(val: Any):
    #     print()
    #     return True
    
    # TODO oh hm also add the namespace information when the config is loaded and not at runtime, might be handy! Oh How to get ctx though? Fizzy says no on that front

class NestedModelData(BaseModel):
    """A potentially incomplete config, allowing for nested inheritance of fields"""
    item: Optional[ListOption[str]]
    reference: Optional[str]
    model: Optional[str|list[dict[str,Any]]] # defalts to reference
    template: Optional[str] = "custom"
    textures: Optional[ListOption[str]]
    broadcast: Optional[list['NestedModelData']] = []

    def collapse_broadcast(self) -> list['NestedModelData']:
        """Recursively collapses broadcast fields into a list of NestedModelData"""
        if not self.broadcast:
            return [self]
        ret_list: list[NestedModelData] = []
        for child in self.broadcast:
            m = NestedModelData.parse_obj(self.dict(exclude_unset=True,exclude={"broadcast"}) | child.dict(exclude_unset=True))
            if m.broadcast:
                m = m.collapse_broadcast()
                ret_list.extend(m)
            else:
                ret_list.append(m)
        return ret_list

class FlatModelDataOptions(BaseModel):
    """Contains a flat list of complete model config objects"""
    model_data: list[ModelData]

class ModelDataOptions(PluginOptions, extra=Extra.ignore):
    model_data: list[NestedModelData] = []

    def process_inheritance(self) -> FlatModelDataOptions:
        """Collapses and returns any broadcast fields into processed flat list"""
        ret: list[ModelData] = []
        errors: list[tuple[int, ValidationError]] = []
        for i, model in enumerate(self.model_data):
            try:
                ret.extend([ModelData(**m.dict()) for m in model.collapse_broadcast()])
            except ValidationError as exc:
                errors.append((i, exc))

        if errors: # generate traceback for configs missing information
            wrapper_errors: list[ErrorWrapper] = []
            for i, error in errors:
                primary_loc = ("model_data", i)
                s = format_validation_error("gm4", ValidationError(model=ModelData, errors=[
                    ErrorWrapper(ValueError(e['msg']), loc=(*primary_loc,*e['loc']))
                    for e in error.errors()
                ]))
                sub_explainations = "\n\t"+"\n\t".join(s.split("\n"))
                wrapper_errors.append(ErrorWrapper(ValueError("a child inherited incomplete options:"+sub_explainations), loc=primary_loc))
            complete_explaination = format_validation_error("gm4", ValidationError(model=ModelData, errors=wrapper_errors))
            raise InvalidOptions("gm4", complete_explaination)
        
        return FlatModelDataOptions(model_data=ret)


def beet_default(ctx: Context):
    rp = ctx.inject(GM4ResourcePack)
    # mecha register

    yield
    rp.output_registry()

def build(ctx: Context):
    rp = ctx.inject(GM4ResourcePack)
    rp.update_modeldata_registry()
    rp.generate_model_overrides()
    rp.generate_model_files()

class GM4ResourcePack():
    """Service Object handling CustomModelData and generated item models"""

    def __init__(self, ctx: Context): # TODO dataclass-ify this?
        self.ctx = ctx
        self.registry = JsonFile(source_path="gm4/modeldata_registry.json").data # TODO caching/save/output this
        self.model_templates = [
            self.custom,
            self.generated,
            self.generated_overlay,
            self.vanilla,
            self.handheld
        ] # TODO init with default templates
        self.logger = parent_logger.getChild(ctx.project_id)

    @cached_property
    def opts(self) -> FlatModelDataOptions:
        # load and process config when it's first accessed. 
        return self.ctx.validate("gm4", validator=ModelDataOptions).process_inheritance()
        # TODO this is where we could pass in the ctx to namespace everything?

    #== Custom Model Data registration and management ==#
    def update_modeldata_registry(self):
        """Updates shared modeldata_registry.json with entries from the beet.yaml"""
        item_registry: dict[str, dict[str, int]] = self.registry.setdefault("items", {})

        # add new references and assign values
        for m in self.opts.model_data:
            ref = add_namespace(m.reference, self.ctx.project_id)
            conflicts = False
            i, err = self.retrieve_index(ref)
            if not err: # existing index, is it available to assign to all items?
                for item_id in m.item.entries():
                    reg = item_registry.setdefault(item_id, {})
                    used_idxs = {k: reg[k] for k in reg.keys() - {ref}}.values()
                    if i in used_idxs:
                        self.logger.warning(f"Failed to share existing CustomModelData for '{ref}' to '{item_id}'. A new value will be assigned for this reference; existing items may lose their texture!")
                        conflicts = True
                if not conflicts: # existing CMD is available to apply to any new items
                    for item_id in [e for e in m.item.entries() if ref not in item_registry.get(e, {})]:
                        self.set_index(item_id, i, ref)
            if err or conflicts: # no existing index, or existing isn't available; get a new one
                self.find_new_index(m.item.entries(), ref)

        # remove unused references
            # NOTE deleting modeldata is really only supported for development cycles. Once published, a cmd value should be permanent.
            # Thus, a reference will only be removed if it is no longer present on *any* item in the beet.yaml
        all_refs = {v for r in self.opts.model_data if (v:=add_namespace(r.reference, self.ctx.project_id)).startswith(self.ctx.project_id)}
        for item_id, reg in item_registry.items():
            for ref in list(reg.keys()):
                if ref.startswith(self.ctx.project_id) and ref not in all_refs:
                    self.logger.info(f"Removing undefined CustomModelData from {item_id} registry: '{ref}'")
                    del reg[ref]
            #FIXME clear references from items no longer configured too


    def generate_model_overrides(self):
        """Generates item model overrides in the 'minecraft' namespace, adding predicates for CustomModelData"""
        
        vanilla = self.ctx.inject(Vanilla)
        vanilla_models_jar = vanilla.mount("assets/minecraft/models/item")
       
        # group models by item id
        for item_id in {i for m in self.opts.model_data for i in m.item.entries()}:
            models = list(filter(lambda m: item_id in m.item.entries(), self.opts.model_data))

            vanilla_model = (v:=vanilla_models_jar.assets.models[f"minecraft:item/{item_id}"].data) | ({} if v.get("overrides") else {"overrides": []})
            vanilla_overrides: list[Any] = vanilla_model["overrides"]
            for override in vanilla_overrides:
                override["model"] = add_namespace(override["model"], "minecraft") # ensure vanilla models have namespaced files
                # FIXME how to differentiate vanilla overrides from specified overrides?
            unchanged_vanilla_overrides = vanilla_overrides.copy()

            filter_func: Callable[[tuple[str, int]], bool] = lambda t: t[0] in [add_namespace(m.reference, self.ctx.project_id) for m in models]
            custom_model_data = dict(filter(filter_func, self.registry["items"][item_id].items()))
            
            for model in models:
                # setup overrides to add CMD to
                if isinstance(model.model, list): # manual predicate merging specified
                    merge_overrides = [o|{"user_defined": True} for o in model.model] # FIXME check branch unnecessary
                else: 
                    merge_overrides = unchanged_vanilla_overrides # get vanilla overrides
                if len(merge_overrides) == 0:
                    merge_overrides.append({}) # add an empty predicate to add CMD onto

                ref = add_namespace(model.reference, self.ctx.project_id)

                for pred in merge_overrides:
                    if not pred.get("model") and not isinstance(model.model, str):
                        self.logger.warn(f"Manually specified model predicate has no 'model' field, and is malformed:\n\t{pred}")
                        continue # TODO this is an exception?
                    vanilla_overrides.append({
                        "predicate": {
                            "custom_model_data": CUSTOM_MODEL_PREFIX+custom_model_data[ref]
                        } | pred.get("predicate", {}),
                        "model": pred["model"] if pred.get("user_defined") else add_namespace(model.model, self.ctx.project_id) # type:ignore , user-defined model predicates use their own model reference. model.model is a string in all other cases
                    })
            self.ctx.assets.models[f"minecraft:item/{item_id}"] = Model(vanilla_model) # TODO skipped-values spacing, on RP output after merge :)

    def retrieve_index(self, reference: str) -> tuple[int, KeyError|Diagnostic|None]:
        """retrieves the CMD value for the given reference"""
        for reg in self.registry["items"].values():
            if reference in reg:
                return reg[reference], None
        return -CUSTOM_MODEL_PREFIX, KeyError(f"{reference} has no asscioated index") # TODO make this Diagnostic
    
    def find_new_index(self, item_ids: list[str], reference: str):
        """finds the next available CMD value for the given items and applies it to the registry"""
        l, u = self.registry["allocations"].get(self.ctx.project_id, (0,99)) # FIXME what happens when the default allocation fills up
        available_indices = set(range(l, u+1))

        for item_id in item_ids:
            used_values = set(self.registry["items"].get(item_id, {}).values())
            available_indices -= used_values

        if not available_indices:
            self.logger.warning("No Valid CMD is open for assignment!") # FIXME this warn
            raise RuntimeError("ran out of CMD to assign") # FIXME
        
        i = min(available_indices)
        self.logger.info(f"Issuing new CustomModelData for '{reference}': {i}")
        for item_id in item_ids:
            self.set_index(item_id, i, reference)
    

    def set_index(self, item_id: str, index: int, reference: str):
        """sets the given cmd index on the item"""
        if os.getenv("GITHUB_ACTIONS"):
            self.logger.error(f"Model-Data cache is outdated. Github Actions cannot issue CustomModelData. Run the build locally and commit changes to modeldata_registry.json")
            sys.exit(1) # stop the build and mark the github action as failed

        self.registry.setdefault("items", {}).setdefault(item_id, {})[reference] = index
        self.logger.info(f"Issuing CustomModelData {index} for {item_id}")

    def output_registry(self):
        # sort registriy alphabetically and numerically
        self.registry["items"] = dict(sorted(self.registry["items"].items()))
        for item_id, ref_map in self.registry["items"].items():
            self.registry["items"][item_id] = dict(sorted(ref_map.items(), key=lambda e: e[1]))

        JsonFile(self.registry).dump(origin="", path="gm4/modeldata_registry.json") # TODO cache this file somehow? Part of RP service exit?

    #== Mecha Transformer Rules ==#
    # TODO

    #== Model file generation and template registration ==#
    def generate_model_files(self):
        """Create individual models for each item/block according to its config"""
        for model in self.opts.model_data:
            if model.textures is None:
                continue # validation should ensure this - here for type checking

            # warn on missing textures
            texs = [add_namespace(t, self.ctx.project_id) for t in model.textures.entries()]
            for tex in texs:
                if tex not in self.ctx.assets.textures:
                    self.logger.warning(f"Referenced texture '{tex}' does not exist") # TODO logger and format as MC messaage
            
            # retrieve model generator function
            try:
                g = next((f for f in self.model_templates if f.__name__ == model.template))
            except StopIteration:
                raise KeyError("template not found") # TODO this error properly
            
            # generate model and mount to the pack
            # TODO redo what data gets passed into the template generators? 
            m = g([add_namespace(t, self.ctx.project_id) for t in model.textures.entries()], model.item)
            if m and isinstance(model.model, str): # pydantic validation ensures type match
                self.ctx.assets.models[add_namespace(model.model, self.ctx.project_id)] = m
    
     # default model templates # FIXME should these be class members? Or generated on init and not bound after that point? Thdy don't have self so maybe not in class
    @staticmethod
    def custom(textures: list[str], *args): # TODO decorator for argument passing? Verification of texture existance?
        """A model file will be provided in source - do not generate a model"""
        return None

    @staticmethod
    def generated(textures: list[str], *args):
        return Model({
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"{textures[0]}" # TODO should this just layer every specified texture?
            }
        })
    
    @staticmethod
    def generated_overlay(textures: list[str], *args): # TODO should this just be default behavior for the "generated" template?
        """A special-case 'generated' template, where an 'overlay' texture is specified by appending '_overlay' to its filename"""
        return Model({
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"{textures[0]}",
                "layer1": f"{textures[0]}_overlay"
            }
        })

    @staticmethod
    def handheld(textures: list[str], *args): # TODO can some of the similar ones be function generated even?
        return Model({
            "parent": "minecraft:item/handheld",
            "textures": {
                "layer0": f"{textures[0]}" # TODO this path correction
            }
        })

    @staticmethod
    def vanilla(textures: list[str], items: ListOption[str]):
        item = items.entries()[0] # TODO should only be one entry?
        return Model({
            "parent": f"minecraft:item/{item}"
        })
    # TODO this should also prevent the texture warnings? Maybe that should be a method of these templates?
