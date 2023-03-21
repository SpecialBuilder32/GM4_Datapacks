from beet import Context, Function, FunctionTag
from beet.contrib.rename_files import rename_files
from beet.contrib.find_replace import find_replace
from gm4.utils import semver_to_dict

def modules(ctx: Context):
    """Assembles version-functions for modules from dependency information:
        - load:{module_name}.json
        - {module_name}:load.mcfunction
        - load:load.json"""
    dependencies: list[str] = ctx.meta.get('gm4', {}).get('required', [])
    lines = ["execute ", ""]

    # {{module_name}}.json tag
    load_tag = dependency_load_tags(ctx, dependencies)
    load_tag.add(f"{ctx.project_id}:load")
    ctx.data.function_tags[f"load:{ctx.project_id}"] = load_tag

    # load.mcfunction
    base_ver = ctx.cache["gm4_manifest"].json["base"]["version"]
    dependencies.insert(0, f"gm4:{base_ver}") # manually insert base version as dependency, assumed to be current base version

    for dep in dependencies:
        dep_id, ver_str = map(lambda s: s.strip(), dep.split(":"))
        dep_ver = semver_to_dict(ver_str)
        name_default_dict = {"name":"Gamemode 4 Base"} if dep_id == "gm4" else {"name":dep_id}
        dep_name: str = ctx.cache["gm4_manifest"].json["modules"].get(dep_id, name_default_dict)["name"]
        
        if dep_id not in ctx.cache["gm4_manifest"].json["modules"] and dep_id != "gm4":
            dep_id = ctx.cache["gm4_manifest"].json["libraries"].get(dep_id)["id"]
        
        # append to startup check
        lines[0] += f"if score {dep_id} load.status matches {dep_ver['major']} if score {dep_id}_minor load.status matches {dep_ver['minor']}.. "

        # failure logs
        lines.append(f"execute unless score {dep_id} load.status matches {dep_ver['major']} unless score {dep_id}_minor load.status matches {dep_ver['minor']}.. run data modify storage gm4:log queue append value {{type:\"missing\",module:\"{ctx.project_name}\",require:\"{dep_name}\"}}")
    
    # finalize startup check
    module_ver = semver_to_dict(ctx.project_version)
    lines[1] = lines[0] + f"run scoreboard players set {ctx.project_id}_minor load.status {module_ver['minor']}"
    lines[0] += f"run scoreboard players set {ctx.project_id} load.status {module_ver['major']}"

    lines.append('')
    # start module clocks
    lines.append(f"execute if score {ctx.project_id} load.status matches {module_ver['major']} run function {ctx.project_id}:init")

    # unschedule clocks
    for function in ctx.meta["gm4"].get("schedule_loops", []):
        namespaced_function = f"{ctx.project_id}:{function}" if ":" not in function else function
        lines.append(f"execute unless score {ctx.project_id} load.status matches {module_ver['major']} run schedule clear {namespaced_function}")

    ctx.data.functions[f"{ctx.project_id}:load"] = Function(lines)

    # load.json tag
    ctx.data.function_tags["load:load"] = FunctionTag({
        "values": [
            f"#load:{ctx.project_id}"
        ]
    })

def libraries(ctx: Context):
    """Assembles version-functions for libraries from dependency information:
        - {lib_name}:enumerate.mcfunction
        - {lib_name}:resolve_load.mcfunction
        - load:{lib_name}.json
        - load:{lib_name}/enumerate.json
        - load:{lib_name}/resolve_load.json
        - load:{lib_name}/dependencies.json"""
    dependencies: list[str] = ctx.meta.get('gm4', {}).get('required', [])
    lib_ver = semver_to_dict(ctx.project_version)

    # enumerate.mcfunction
    lines = [
        f"execute if score {ctx.project_id} load.status matches {lib_ver['major']} unless score {ctx.project_id}_minor load.status matches {lib_ver['minor']}.. run scoreboard players set {ctx.project_id}_minor load.status {lib_ver['minor']}",
        "",
    ]

    dep_check_line = "execute "
    for dep in dependencies:
        dep_id, ver_str = map(lambda s: s.strip(), dep.split(":"))
        dep_ver = semver_to_dict(ver_str)

        if dep_id not in ctx.cache["gm4_manifest"].json["modules"]:
            dep_id = ctx.cache["gm4_manifest"].json["libraries"].get(dep_id)["id"]
        
        dep_check_line += f"if score {dep_id} load.status matches {dep_ver['major']} if score {dep_id}_minor load.status matches {dep_ver['minor']}.. "

    dep_check_line += f"unless score {ctx.project_id} load.status matches 1.. run scoreboard players set "

    lines.append(dep_check_line + f"{ctx.project_id}_minor load.status {lib_ver['minor']}")
    lines.append(dep_check_line + f"{ctx.project_id} load.status {lib_ver['major']}")

    ctx.data.functions[f"{ctx.project_id}:enumerate"] = Function(lines)

    # resolve_load.mcfunction
    lines = [f"execute if score {ctx.project_id} load.status matches {lib_ver['major']} if score {ctx.project_id}_minor load.status matches {lib_ver['minor']} run function {ctx.project_id}:load"]

    for func in ctx.meta["gm4"].get("schedule_loops", []):
        lines.append(f"execute unless score {ctx.project_id} load.status matches {lib_ver['major']} run schedule clear {ctx.project_id}:{func}")
        lines.append(f"execute unless score {ctx.project_id}_minor load.status matches {lib_ver['minor']} run schedule clear {ctx.project_id}:{func}")
        
    ctx.data.functions[f"{ctx.project_id}:resolve_load"] = Function(lines)

    # load/tags {{ lib name }}.json
    ctx.data.function_tags[f"load:{ctx.project_id}"] = FunctionTag({
        "values": [
            f"#load:{ctx.project_id}/enumerate",
            f"#load:{ctx.project_id}/resolve_load"
        ]
    })

    # load/tags enumerate.json
    ctx.data.function_tags[f"load:{ctx.project_id}/enumerate"] = FunctionTag({
        "values": [
            f"{ctx.project_id}:enumerate"
        ]
    })

    # load/tags resolve_load.json
    ctx.data.function_tags[f"load:{ctx.project_id}/resolve_load"] = FunctionTag({
        "values": [
            f"{ctx.project_id}:resolve_load"
        ]
    })

    # load/tags dependencies.json
    if len(dependencies) > 0:
        dep_tag = dependency_load_tags(ctx, dependencies)
        ctx.data.function_tags[f"load:{ctx.project_id}/dependencies"] = dep_tag
        ctx.data.function_tags[f"load:{ctx.project_id}"].prepend(FunctionTag({
            "values": [
                f"#load:{ctx.project_id}/dependencies"
            ]
        }))

    yield # wait for all pack files to load

    # additional version injections
    extra_injections = ctx.meta["gm4"].get("extra_version_injections", {})

    # NOTE functions get version checks replaced onto `load.status` checks
    ctx.require(find_replace(data_pack={"match": {
        "functions": [f if ':' in f else f"{ctx.project_id}:{f}" for f in extra_injections.get("functions", [])]}
        },
        substitute={
            "find": f"{ctx.project_id} load\\.status matches \\d(?: if score {ctx.project_id}_minor load\\.status matches \\d)?",
            "replace": f"{ctx.project_id} load.status matches {lib_ver['major']} if score {ctx.project_id}_minor load.status matches {lib_ver['minor']}"
        }
    ))

    # NOTE advancements get score checks injected into every criteria
    for entry in extra_injections.get("advancements", []):
        handle = ctx.data.advancements[f"{ctx.project_id}:{entry}"]
        for criteria in handle.data["criteria"].values():
            player_conditions = criteria.setdefault("conditions", {}).setdefault("player", [])
            player_conditions.append({
                "condition": "minecraft:value_check",
                "value": {
                "type": "minecraft:score",
                "target": {
                    "type": "minecraft:fixed",
                    "name": f"{ctx.project_id}"
                },
                "score": "load.status"
                },
                "range": lib_ver["major"]
            })
            player_conditions.append({
                "condition": "minecraft:value_check",
                "value": {
                "type": "minecraft:score",
                "target": {
                    "type": "minecraft:fixed",
                    "name": f"{ctx.project_id}_minor"
                },
                "score": "load.status"
                },
                "range": lib_ver["minor"]
            })

    # namespace renaming to include version number
    versioned_namespace = f"{ctx.project_id}-{lib_ver['major']}.{lib_ver['minor']}"
    ctx.require(rename_files(data_pack={
        "match":{"functions": "*", "advancements": "*", "loot_tables": "*", "predicates": "*"},
        "find": f"{ctx.project_id}:([a-z_/]+)",
        "replace": f"{versioned_namespace}:\\1"
    }))
    ctx.require(find_replace(data_pack={"match": "*"}, substitute={
        "find": f"(?<!#)(?<!storage ){ctx.project_id}:([a-z0-9_/]+)",
        "replace": f"{versioned_namespace}:\\1"
    }))
    

def dependency_load_tags(ctx: Context, dependencies: list[str]) -> FunctionTag:
    """Assembles dependency information into tag format. Ensures a pack's dependencies
    get processed by lantern load before the primary startup checks for the module itself"""
    dep_tag = FunctionTag()
    for dep in dependencies:
        if ":" not in dep:
            raise ValueError(f"{ctx.project_id} has a dependancy without a specified version; {dep}")
        dep_id, _ = map(lambda s: s.strip(), dep.split(":"))
        if dep_id not in ctx.cache["gm4_manifest"].json["modules"]:
            dep_id = ctx.cache["gm4_manifest"].json["libraries"].get(dep_id)["id"]
        dep_tag.append(FunctionTag(
            {"values":[
                {"id": f"#load:{dep_id}", "required": False}
            ]}
        ))
    return dep_tag

def cache_premodule_advancements(ctx: Context):
    """Stores advancements loaded in ctx right before the actual module data is loaded. 
    Used to add version/startup checks to module-level advancements in versioning.module"""
    ctx.meta["premodule_advancements"] = list(ctx.data.advancements.keys())

def module_load_advancements(ctx: Context):
    """Injects module load success checks (load.status 1..) into technical and display advancements for each module"""
        # advancements get score checks injected into every criteria
    base_exclusions = ["gm4:root", "gm4_intro_song:intro_song"] # manually set list to avoid checking base for advancements when it doesn't change module to module
    for name in [a for a in ctx.data.advancements.keys() if a not in ctx.meta.get("premodule_advancements", []) + base_exclusions]:
        handle = ctx.data.advancements[name]
        for criteria in handle.data["criteria"].values():
            player_conditions = criteria.setdefault("conditions", {}).setdefault("player", [])
            if type(player_conditions) is dict:
                raise ValueError(f"{name} is using legacy player conditions, which does not support load.status injections.")
            player_conditions.append({
                "condition": "minecraft:value_check",
                "value": {
                "type": "minecraft:score",
                "target": {
                    "type": "minecraft:fixed",
                    "name": f"{ctx.project_id}"
                },
                "score": "load.status"
                },
                "range": {
                    "min": 1
                }
            })