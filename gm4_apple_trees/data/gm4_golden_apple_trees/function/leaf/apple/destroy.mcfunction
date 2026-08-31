# removes a ripe apple leaf item display if it is not inside a leaf anymore
# @s = gm4_ripe_apple item display that's holding an apple
# located at @s
# run from gm4_apple_trees:leaf/destroy

# drop apple
execute if predicate gm4_golden_apple_trees:apple_in_display positioned ^0.25 ^-0.7 ^  run function gm4_golden_apple_trees:leaf/apple/drop

# kill
kill @s
