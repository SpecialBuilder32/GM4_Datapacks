#@s = fishing bobber
#run from pulse_check

summon minecraft:armor_stand ^ ^ ^-3 {DisabledSlots:2039552,Invisible:1,NoGravity:1b,Tags:["gm4_no_edit","gm4_fishing_bait_set"]}

scoreboard players operation @e[type=armor_stand,limit=1,sort=nearest,tag=gm4_fishing_bait_set] gm4_ef_id = @s gm4_ef_id

scoreboard players operation @e[type=armor_stand,limit=1,sort=nearest,tag=gm4_fishing_bait_set] gm4_ef_lure = @s gm4_ef_lure

execute as @e[type=armor_stand,limit=1,sort=nearest,tag=gm4_fishing_bait_set] run function end_fishing:cast_rod/randomize_timer

tag @e[type=armor_stand,limit=1,sort=nearest,tag=gm4_fishing_bait_set] add gm4_fishing_bait
tag @e[type=armor_stand,limit=1,sort=nearest,tag=gm4_fishing_bait_set] remove gm4_fishing_bait_set

tag @s add gm4_ef_casted
