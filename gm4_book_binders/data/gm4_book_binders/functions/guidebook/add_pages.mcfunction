# adds pages to the guidebook
# @s = player who's updating their guidebook
# located at @s
# run from gm4_book_binders:guidebook/verify_module

data modify storage gm4_guidebook:temp insert set value ['','["",{"text":"◀ ","color":"#4AA0C7","clickEvent":{"action":"change_page","value":"2"},"hoverEvent":{"action":"show_text","contents":[{"translate":"%1$s%3427655$s","with":[{"text":"Return to Table of Contents"},{"translate":"text.gm4.guidebook.return_to_table"}],"italic":true,"color":"gold"}]}},{"translate":"%1$s%3427655$s","with":[{"text":"Back"},{"translate":"text.gm4.guidebook.back"}],"color":"#4AA0C7","clickEvent":{"action":"change_page","value":"2"},"hoverEvent":{"action":"show_text","contents":[{"translate":"%1$s%3427655$s","with":[{"text":"Return to Table of Contents"},{"translate":"text.gm4.guidebook.return_to_table"}],"italic":true,"color":"gold"}]}},{"text":"\\n"},{"text":"☶ ","color":"#864BC7","bold":true,"clickEvent":{"action":"open_url","value":"https://wiki.gm4.co/wiki/Book_Binders"},"hoverEvent":{"action":"show_text","contents":[{"translate":"%1$s%3427655$s","with":[{"text":"Open External Wiki"},{"translate":"text.gm4.guidebook.open_wiki"}],"italic":true,"color":"gold"}]}},{"translate":"%1$s%3427655$s","with":[{"text":"Wiki"},{"translate":"text.gm4.guidebook.wiki"}],"color":"#864BC7","clickEvent":{"action":"open_url","value":"https://wiki.gm4.co/wiki/Book_Binders"},"hoverEvent":{"action":"show_text","contents":[{"translate":"%1$s%3427655$s","with":[{"text":"Open External Wiki"},{"translate":"text.gm4.guidebook.open_wiki"}],"italic":true,"color":"gold"}]}},{"text":"\\n\\n"},{"text":"Book Binders","underlined":true},{"text":"\\n"},{"translate":"%1$s%3427655$s","with":[{"text":"Lecterns have a small area at the center where enchanted books can be placed. This will cause the enchanted book to be ripped up into separate pages—one for each enchantment."},{"translate":"text.gm4.guidebook.book_binders.1"}]}]','["",{"text":"???","hoverEvent":{"action":"show_text","contents":[{"translate":"%1$s%3427655$s","with":[{"text":"Undiscovered"},{"translate":"text.gm4.guidebook.undiscovered"}],"italic":true,"color":"red"}]}}]','["",{"text":"???","hoverEvent":{"action":"show_text","contents":[{"translate":"%1$s%3427655$s","with":[{"text":"Undiscovered"},{"translate":"text.gm4.guidebook.undiscovered"}],"italic":true,"color":"red"}]}}]']

# unlockable pages
execute if entity @s[advancements={gm4_guidebook:book_binders/page_1=true}] run data modify storage gm4_guidebook:temp insert[2] set value '["",{"translate":"%1$s%3427655$s","with":[{"text":"Placing enchanted pages onto a lectern will add it to its internal inventory. Placing a leather onto the lectern will then bind the pages in its inventory, creating an enchanted book."},{"translate":"text.gm4.guidebook.book_binders.2"}]}]'
execute if entity @s[advancements={gm4_guidebook:book_binders/page_1=true}] run data modify storage gm4_guidebook:temp insert[3] set value '["",{"translate":"%1$s%3427655$s","with":[{"text":"A hopper feeding into the back of the lectern will push items into it and a hopper below the lectern will catch any items dropped by the lectern."},{"translate":"text.gm4.guidebook.book_binders.3"}]}]' 