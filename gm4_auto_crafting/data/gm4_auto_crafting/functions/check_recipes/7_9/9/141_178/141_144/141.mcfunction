scoreboard players reset * gm4_craft_shapeless
execute if score $crafted gm4_crafting matches 0 if score $stack_size gm4_crafting matches ..8 store result score $minecraft:sand gm4_craft_shapeless if data storage gm4_custom_crafters:temp/crafter Items[{id:"minecraft:sand"}]
execute if score $minecraft:sand gm4_craft_shapeless matches 4 store result score $minecraft:gravel gm4_craft_shapeless if data storage gm4_custom_crafters:temp/crafter Items[{id:"minecraft:gravel"}]
execute if score $minecraft:gravel gm4_craft_shapeless matches 4 store result score $crafted gm4_crafting if data storage gm4_custom_crafters:temp/crafter {Items:[{id:"minecraft:magenta_dye"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/magenta_concrete_powder
execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches ..8 if data storage gm4_custom_crafters:temp/crafter {Items:[{Slot:0b,id:"minecraft:glass"},{Slot:1b,id:"minecraft:glass"},{Slot:2b,id:"minecraft:glass"},{Slot:3b,id:"minecraft:glass"},{Slot:4b,id:"minecraft:magenta_dye"},{Slot:5b,id:"minecraft:glass"},{Slot:6b,id:"minecraft:glass"},{Slot:7b,id:"minecraft:glass"},{Slot:8b,id:"minecraft:glass"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/magenta_stained_glass
