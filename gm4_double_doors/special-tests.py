from beet import subproject, Context
from beet.contrib.vanilla import Vanilla

def beet_default(ctx: Context):
    vanilla = ctx.inject(Vanilla)
    wooden_doors = vanilla.data.block_tags["minecraft:wooden_doors"]
    
    for wood_type in [s.removeprefix("minecraft:").removesuffix("_door") for s in wooden_doors.data["values"]]:
        subproject_config = {
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
                    # "structures": "*"
                }
            },
            "meta":{
                "material_type": wood_type
            }
        }

        ctx.require(subproject(subproject_config))
