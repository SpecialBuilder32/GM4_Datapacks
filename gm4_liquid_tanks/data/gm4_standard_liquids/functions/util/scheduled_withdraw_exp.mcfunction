# scheduled from standard_liquids:util_below

execute as @e[type=armor_stand,tag=gm4_liquid_tank,tag=gm4_lt_experience] at @s if block ~ ~ ~ hopper[enabled=true] positioned ~ ~-2 ~ if entity @a[distance=..0.5,gamemode=!spectator] if score @s gm4_lt_value matches 1.. run function gm4_standard_liquids:util/withdraw_experience

schedule function gm4_standard_liquids:util/scheduled_withdraw_exp 1t