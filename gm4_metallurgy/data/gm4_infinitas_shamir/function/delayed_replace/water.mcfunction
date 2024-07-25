# Checks which hand slot player used to place water
# @s = player holding water bucket, previously holding Infinitas Water Bucket
# at @s
# run from gm4_infinitas_shamir:delayed_replace/check_tag

execute store success score @s gm4_infinitas_success_check run item replace entity @s[predicate=gm4_infinitas_shamir:mainhand/after/water,predicate=gm4_infinitas_shamir:mainhand/after/water_advancement] weapon.mainhand with water_bucket
execute if score @s gm4_infinitas_success_check matches 1 run item modify entity @s weapon.mainhand gm4_infinitas_shamir:restore_shamir
execute store success score @s gm4_infinitas_success_check run item replace entity @s[predicate=gm4_infinitas_shamir:offhand/after/water,predicate=gm4_infinitas_shamir:offhand/after/water_advancement] weapon.offhand with water_bucket
execute if score @s gm4_infinitas_success_check matches 1 run item modify entity @s weapon.offhand gm4_infinitas_shamir:restore_shamir

# clean up
advancement revoke @s only gm4_infinitas_shamir:water/place
tag @s remove gm4_infinitas_delay_replace
tag @s remove gm4_infinitas_delay_replace_water
