execute unless score apple_trees gm4_modules matches 1 run data modify storage gm4:log queue append value {type:"install",module:"Apple Trees"}
scoreboard players set apple_trees gm4_modules 1

# scoreboards and constants
scoreboard objectives add gm4_apple_data dummy
scoreboard players set #max_height gm4_apple_data 5
scoreboard players set #min_height gm4_apple_data 3

scoreboard players set #stage_1_start gm4_apple_data 10
scoreboard players set #stage_2_start gm4_apple_data 20
scoreboard players set #stage_0_start gm4_apple_data 30
