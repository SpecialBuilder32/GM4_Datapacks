# sets this apple leaf's stage to 2
# @s = gm4_apple item_display on stage 1 (small apple) which should drop its apple
# located at @s align xyz
# run from gm4_apple_trees:tree/leaf/fruiting/advance_stage

# set leaf's next stage change age
scoreboard players operation @s gm4_fruit_stage = #stage_0_start gm4_apple_data

# visuals
playsound minecraft:block.beehive.drip block @a[distance=..8] ~ ~ ~ 0.3 1.4
item replace entity @s contents with minecraft:apple 1
tag @s add gm4_ripe_apple
