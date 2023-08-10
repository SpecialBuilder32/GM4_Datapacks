from typing import ClassVar

from beet import Context, Structure, TextFile, subproject
from beet.contrib.vanilla import Vanilla
from nbtlib import parse_nbt


class StringStructure(TextFile):
    scope: ClassVar[tuple[str, ...]] = ("structures",)
    extension: ClassVar[str] = ".snbt"

    def serialize_to_structure(self) -> Structure:
        return Structure(parse_nbt(self.text))

def register_snbt_files(ctx: Context):
    ctx.data.extend_namespace.append(StringStructure)


def beet_default(ctx: Context):
    vanilla = ctx.inject(Vanilla)
    wooden_doors = vanilla.data.block_tags["minecraft:wooden_doors"]
    
    for wood_type in [s.removeprefix("minecraft:").removesuffix("_door") for s in wooden_doors.data["values"]]:
        subproject_config = {
            "require": [
                "gm4_double_doors.special-tests.register_snbt_files"
            ],
            "data_pack":{
                "load": [
                    {
                        f"data/gm4_double_doors/advancements/{wood_type}": "data/gm4_double_doors/templates/advancements",
                        f"data/gm4_double_doors/functions/{wood_type}": "data/gm4_double_doors/templates/functions",
                        f"data/gm4_double_doors/structures/{wood_type}": "data/gm4_double_doors/templates/structures",
                    }
                ],
                "render":{
                    "advancements": "*",
                    "functions": "*",
                    "string_structures": "*" # renders all mounted files of the StringStructure container
                }
            },
            "meta":{
                "material_name": wood_type
            }
        }

        ctx.require(subproject(subproject_config))

    for name, struct in ctx.data[StringStructure].items():
        ctx.data[Structure][name] = struct.serialize_to_structure()
    ctx.data[StringStructure].clear()
