# run from gm4_potion_liquids:item_drain
# @s = tank being processed

scoreboard players set $item_value gm4_lt_value 3
data merge storage gm4_liquid_tanks:temp/tank {output:{id:"glass_bottle"}}
function gm4_liquid_tanks:smart_item_drain
tag @s add gm4_lt_drain

