# Python program to read
# json file
import json
  
def get_json_data():
    f = open('platformer/data/map_data.json',)
    data = json.load(f)
    f.close()

    return data