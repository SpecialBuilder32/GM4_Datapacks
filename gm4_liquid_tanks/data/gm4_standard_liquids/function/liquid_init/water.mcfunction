data merge block ~ ~ ~ {CustomName:'{"translate":"gm4.second","fallback":"%1$s","with":[{"translate":"container.gm4.liquid_tank.water","fallback":"Water Tank"},[{"translate":"gui.gm4.liquid_tank","fallback":"","font":"gm4:container_gui","color":"white"},{"translate":"container.gm4.liquid_tank.water","fallback":"Water Tank","font":"gm4:default","color":"#404040"}]]}'}
summon armor_stand ~ ~-.95 ~ {CustomName:'"gm4_liquid_tank_display"',Tags:["gm4_no_edit","gm4_liquid_tank_display","smithed.entity","smithed.strict"],NoGravity:1b,Marker:1b,Invisible:1b,Invulnerable:1b,Small:1b,Silent:1b,DisabledSlots:4144959,HasVisualFire:1b,ArmorItems:[{},{},{},{id:"player_head",count:1,components:{"minecraft:profile":"$gm4_standard_liquids:liquids/water"}}]}
data modify entity @s data.gm4_liquid_tanks.liquid_tag set value "gm4_lt_water"
scoreboard players set @s gm4_lt_max 300
tag @s add gm4_lt_water
tag @s remove gm4_lt_empty
