from beet import subproject, Context

def beet_default(ctx: Context):
    ctx.require(subproject({
        "data_pack":{
            "load": [
                {
                    "data/gm4_double_doors/advancements/oak": "data/gm4_double_doors/templates/advancements",
                    "data/gm4_double_doors/functions/oak": "data/gm4_double_doors/templates/functions",
                    "data/gm4_double_doors/structures/oak": "data/gm4_double_doors/templates/structures",
                }
            ],
            "render":{
                "advancements": "*",
                "functions": "*",
                # "structures": "*"
            }
        },
        "meta":{
            "material_name": "oak"
        }
    }))
