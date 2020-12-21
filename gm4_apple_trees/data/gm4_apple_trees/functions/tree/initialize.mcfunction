# initializes the apple tree's scores
# @s = sapling marker area_effect_cloud
# at @s align xyz
# run from gm4_fruiting_trees:generate via #gm4_fruiting_trees:initialize

# determine available height
scoreboard players set $max_layer gm4_tree_layer 0
function gm4_apple_trees:tree/layer/check_clear_space
# $max_layer is now the height available to the tree to grow
execute if score $max_layer gm4_tree_layer < #min_height gm4_apple_data run scoreboard players set $cancel_generation gm4_tree_layer 1
