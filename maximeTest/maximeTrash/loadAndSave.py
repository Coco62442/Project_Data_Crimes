import json

f = open("../originalData/departements-version-simplifiee.geojson")

data = json.load(f)
print(data['features'][0]["properties"])
data['features'][0]["properties"]["years"] = {
  "2019": {
    "crime": 1,
    "mort" :2
  },
  "2020": {
    "crime": 1,
    "mort" :2
  },
  "2021": {
    "crime": 1,
    "mort" :2
  }
}

print(data['features'][0]["properties"]["years"])

with open(f'TEST.json', 'w') as json_file:
    json.dump(data, json_file)

f.close()