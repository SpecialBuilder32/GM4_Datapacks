execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches ..64 if data storage gm4_custom_crafters:temp/crafter {Items:[{id:"minecraft:ender_pearl"},{id:"minecraft:blaze_powder"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/ender_eye
execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches 1 if data storage gm4_custom_crafters:temp/crafter {Items:[{id:"minecraft:white_bed"},{id:"minecraft:light_blue_dye"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/light_blue_bed_from_white_bed
execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches 1 if data storage gm4_custom_crafters:temp/crafter {Items:[{id:"minecraft:white_bed"},{id:"minecraft:light_gray_dye"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/light_gray_bed_from_white_bed
execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches ..64 if data storage gm4_custom_crafters:temp/crafter {Items:[{id:"minecraft:exposed_copper"},{id:"minecraft:honeycomb"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/waxed_exposed_copper_from_honeycomb
