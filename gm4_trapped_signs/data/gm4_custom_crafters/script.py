import json

with open("gm4_trapped_signs/data/gm4_custom_crafters/gm4_trapped_signs.json", 'r') as f:
    data = json.load(f)

for r in data:
    with open(f"gm4_trapped_signs/data/gm4_trapped_signs/gm4_recipes/{r['name'].removeprefix('gm4_trapped_signs:')}.json", 'w') as f:
        json.dump(r, f)
