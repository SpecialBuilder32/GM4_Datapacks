#@s = water tank with one written book in the first slot
#run from wash

scoreboard players set $item_value gm4_lt_value -1
data merge storage gm4_liquid_tanks:temp/tank {output:{id:"book"}}
function gm4_liquid_tanks:smart_item_drain
tag @s add gm4_lt_fill
