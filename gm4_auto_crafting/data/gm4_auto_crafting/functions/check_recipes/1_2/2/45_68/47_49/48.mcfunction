execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches ..64 if data storage gm4_custom_crafters:temp/crafter {Items:[{Slot:0b,id:"minecraft:sandstone_slab"},{Slot:3b,id:"minecraft:sandstone_slab"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/chiseled_sandstone
execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches ..64 if data storage gm4_custom_crafters:temp/crafter {Items:[{Slot:0b,id:"minecraft:crimson_planks"},{Slot:1b,id:"minecraft:crimson_planks"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/crimson_pressure_plate
execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches ..16 if data storage gm4_custom_crafters:temp/crafter {Items:[{Slot:0b,id:"minecraft:blaze_rod"},{Slot:3b,id:"minecraft:popped_chorus_fruit"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/end_rod
execute if score $crafted gm4_crafting matches 0 store success score $crafted gm4_crafting if score $stack_size gm4_crafting matches ..64 if data storage gm4_custom_crafters:temp/crafter {Items:[{id:"minecraft:oxidized_cut_copper"},{id:"minecraft:honeycomb"}]} run loot replace block ~ ~ ~ container.0 loot gm4_auto_crafting:crafting/vanilla/waxed_oxidized_cut_copper_from_honeycomb
