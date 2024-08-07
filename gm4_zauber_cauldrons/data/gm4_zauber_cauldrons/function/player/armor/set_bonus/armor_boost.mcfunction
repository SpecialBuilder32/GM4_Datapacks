# applies a set bonus and displays some particles
# @s = player who's inventory changed and now has full armor_boost armor
# at @s
# run from player/armor/apply_set_bonus

# attribute
attribute @s minecraft:generic.armor modifier add minecraft:b29259d8-1ac4-4791-9552-b944910cd435 1 add_value

# sounds and visuals
particle minecraft:entity_effect{color:[0.561,0.271,0.929,1.0]} ~.3 ~.8 ~.3 0 0 0 1 1
particle minecraft:entity_effect{color:[0.561,0.271,0.929,1.0]} ~.3 ~.8 ~-.3 0 0 0 1 1
particle minecraft:entity_effect{color:[0.561,0.271,0.929,1.0]} ~-.3 ~.8 ~-.3 0 0 0 1 1
particle minecraft:entity_effect{color:[0.561,0.271,0.929,1.0]} ~-.3 ~.8 ~.3 0 0 0 1 1
particle minecraft:entity_effect{color:[0.561,0.271,0.929,1.0]} ^ ^1.2 ^0.1 0 0 0 1 1
particle minecraft:entity_effect{color:[0.561,0.271,0.929,1.0]} ^ ^1.2 ^-0.1 0 0 0 1 1
particle minecraft:entity_effect{color:[0.561,0.271,0.929,1.0]} ^0.1 ^1.2 ^ 0 0 0 1 1
particle minecraft:entity_effect{color:[0.561,0.271,0.929,1.0]} ^-0.1 ^1.2 ^ 0 0 0 1 1
playsound minecraft:block.beacon.power_select player @a[distance=..4] ~ ~ ~ 0.2 1.55
