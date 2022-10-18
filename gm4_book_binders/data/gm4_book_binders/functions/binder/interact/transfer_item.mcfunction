# @s = player interacting with binder
# at corner of lectern block
# run from binder/interact/ray

execute store success score $success gm4_binder_data run item replace entity @e[type=armor_stand,tag=gm4_book_binder,limit=1,dx=0,dy=0,dz=0] weapon.mainhand from entity @s weapon.mainhand gm4_book_binders:set_count_one

execute if score $success gm4_binder_data matches 1 run item modify entity @s[gamemode=!creative] weapon.mainhand gm4_book_binders:decrement_stack
execute if score $success gm4_binder_data matches 1 run playsound minecraft:item.book.put block @a[distance=..10] ~ ~ ~ 1 1