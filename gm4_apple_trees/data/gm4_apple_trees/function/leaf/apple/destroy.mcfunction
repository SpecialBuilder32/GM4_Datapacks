# removes a ripe apple leaf item display if it is not inside a leaf anymore
# @s = gm4_ripe_apple item_display that's holding an apple
# located at @s
# run from gm4_apple_trees:leaf/destroy

# drop apple
execute if predicate gm4_apple_trees:apple_holding positioned ~0.5 ~2.5 ~0.5 positioned ^-.25 ^ ^.1 run function gm4_apple_trees:leaf/apple/drop

# kill
kill @s
