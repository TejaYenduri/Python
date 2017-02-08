import ijson

filename = "/Users/PammuTeha/Documents/Python/device42-script/cache/buildings_cache.json"
columns = None
with open(filename, 'r') as f:
    objects = ijson.items(f, 'item')
    columns = list(objects)
print columns[0]
