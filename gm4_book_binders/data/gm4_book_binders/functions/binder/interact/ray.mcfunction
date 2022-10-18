# @s = player interacting with lectern
# at current ray-cast-position in front of eyes
# run from binder/interact/lectern_interact and self

scoreboard players remove $ray gm4_binder_data 1

execute if block ~ ~ ~ lectern align xyz run function gm4_book_binders:binder/interact/transfer_item

execute unless block ~ ~ ~ lectern unless score $ray gm4_binder_data matches ..0 positioned ^ ^ ^0.1 run function gm4_book_binders:binder/interact/ray

