
data modify storage gm4_combat_expanded:temp wild_magic.id set value "wither"

# Duration
execute store result storage gm4_combat_expanded:temp wild_magic.duration int 1 run random value 6..20

# Level
scoreboard players set $add gm4_ce_data 2
execute store result storage gm4_combat_expanded:temp wild_magic.level int 1 run loot spawn 29999998 1 7133 loot gm4_combat_expanded:technical/wild_magic_level
