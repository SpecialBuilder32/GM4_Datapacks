# @s = player interacting with lectern
# at @s
# run from advancement gm4_book_binders:interact_with_lectern 

advancement revoke @s only gm4_book_binders:interact_with_lectern

# raycast to lectern block and transfer item
scoreboard players set $ray gm4_binder_data 50
execute anchored eyes run function gm4_book_binders:binder/interact/ray
# raycase executes binder/interact/transfer_item at lectern