scoreboard objectives add gm4_animi_deaths deathCount
scoreboard objectives add gm4_animi_leave minecraft.custom:minecraft.leave_game

execute unless score animi_shamir gm4_modules matches 1 run data modify storage gm4:log queue append value {type:"install",module:"Animi Shamir"}
execute unless score animi_shamir gm4_earliest_version < animi_shamir gm4_modules run scoreboard players operation animi_shamir gm4_earliest_version = animi_shamir gm4_modules
scoreboard players set animi_shamir gm4_modules 1

# register shamir with lib_player_heads
execute unless data storage gm4_player_heads:register heads[{id:"gm4_animi_shamir:band/v0"}] run data modify storage gm4_player_heads:register heads append value {id:"gm4_animi_shamir:band/v1",name:"[Drop to Fix Item] gm4_animi_shamir:band/v0",item:{gm4_metallurgy:{has_shamir:1b,stored_shamir:"animi",metal:{type:"curies_bismium",amount:[9s,3s],castable:1b},item:"obsidian_cast"},SkullOwner:{Id:[I;-1332644679,659216762,2108439484,664728976],Properties:{textures:[{Value:"ewogICJ0aW1lc3RhbXAiIDogMTYyODAyOTI2NzM2NiwKICAicHJvZmlsZUlkIiA6ICI3ZmIyOGQ1N2FhZmQ0MmQ1YTcwNWNlZjE4YWI1MzEzZiIsCiAgInByb2ZpbGVOYW1lIiA6ICJjaXJjdWl0MTAiLAogICJzaWduYXR1cmVSZXF1aXJlZCIgOiB0cnVlLAogICJ0ZXh0dXJlcyIgOiB7CiAgICAiU0tJTiIgOiB7CiAgICAgICJ1cmwiIDogImh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvM2MzMTBmZDk3YjFhN2Q3MDkwOGExODc2N2FjZmRjYzYwZDJhMTU1NTY5Zjk0YThmYjZhZWUxYTMzMWE5MjM4IgogICAgfQogIH0KfQ=="}]}},CustomModelData:3420117,display:{Name:'{"italic":false,"translate":"item.gm4.metallurgy.obsidian_cast","fallback":"Obsidian Cast"}',Lore:['{"italic":false,"color":"#467A1B","translate":"item.gm4.metallurgy.band","fallback":"Curie\'s Bismium Band","with":[{"translate":"item.gm4.metallurgy.curies_bismium"}]}','{"italic":false,"color":"aqua","translate":"item.gm4.metallurgy.shamir","fallback":"Shamir"}','{"italic":false,"color":"gray","translate":"item.gm4.shamir.animi","fallback":"Animi"}']}}}

# guidebook
execute if score gm4_guidebook load.status matches 1 run summon marker ~ 315.331110999018 ~ {CustomName:'"gm4_animi_shamir_guide"',Tags:["gm4_guide"],data:{type:"_expansion",base:"metallurgy",id:"animi_shamir",page_count:2,line_count:1,module_name:"Animi Shamir"}}

#$moduleUpdateList