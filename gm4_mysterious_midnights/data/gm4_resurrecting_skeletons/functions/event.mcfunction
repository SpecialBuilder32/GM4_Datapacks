#@s = none
#at world spawn
#called by mysterious midnights base if this expansion was selected. pulsed every 0.8 seconds throughout the night.

execute as @e[type=item,x=0] if items entity @s contents minecraft:bone if entity @s[nbt={OnGround:1b}] run function gm4_resurrecting_skeletons:mark_bone
execute as @e[type=item,scores={gm4_reskelify=8..}] at @s run function gm4_resurrecting_skeletons:spawn_skeleton
