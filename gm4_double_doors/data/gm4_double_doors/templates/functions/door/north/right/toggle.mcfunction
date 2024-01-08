# Toggles the double door the player has interacted with.
# @s = player that interacted with a door
# at location of the lower half of the left door of the double door the player has interacted with
# run from check_neighbours functions in gm4_double_doors:{{ material_name }}/door/...

# player just closed a door
execute if score $target_door_state gm4_double_doors_data matches 0 run place template gm4_double_doors:{{ material_name }}/door/north/right/closed ~ ~ ~

# player just opened a door
execute if score $target_door_state gm4_double_doors_data matches 1 run place template gm4_double_doors:{{ material_name }}/door/north/right/open ~ ~ ~

# get target trapdoor state (0->0, 1->1 for this direction)
execute store result score $target_trapdoor_state gm4_double_doors_data if score $target_door_state gm4_double_doors_data matches 1

# check for potential trapdoors which should also be opened
scoreboard players operation $trap_door_recursion_level gm4_double_doors_data = $trap_door_limit gm4_double_doors_data
execute positioned ~ ~2 ~ if block ~ ~ ~ minecraft:{{ material_name }}_trapdoor[open=true,half=bottom] unless block ~ ~ ~ minecraft:{{ material_name }}_trapdoor[facing=east] unless block ~ ~ ~ minecraft:{{ material_name }}_trapdoor[facing=south] run function gm4_double_doors:{{ material_name }}/trapdoor/north_west/check_neighbours

# prepare automatic un-toggling after player walked through, delete preexisting auto toggle markers
execute align xyz run kill @e[type=marker,tag=gm4_double_doors_auto_toggle_marker,dx=0]
execute unless score $triggered_by_auto_toggle gm4_double_doors_data matches 1.. summon marker run function gm4_double_doors:{{ material_name }}/door/north/right/initialize_auto_toggle_marker
execute if score $triggered_by_auto_toggle gm4_double_doors_data matches 1.. run scoreboard players set $play_sound gm4_double_doors_data 1
