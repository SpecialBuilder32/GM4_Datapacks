# TODO
# @s = player that interacted with a door
# at location of the lower half of the door the player has interacted with
# run from TODO

# open this trapdoor
function gm4_double_doors:trapdoor/south_west/toggle

# check for potential trapdoors which should also be opened
scoreboard players remove $trap_door_recursion_level gm4_double_doors_data 1
execute if score $trap_door_recursion_level gm4_double_doors_data matches 1.. positioned ~ ~1 ~ if block ~ ~ ~ #minecraft:trapdoors[open=true,half=bottom] unless block ~ ~ ~ #minecraft:trapdoors[facing=east] unless block ~ ~ ~ #minecraft:trapdoors[facing=north] run function gm4_double_doors:trapdoor/south_west/check_neighbours
