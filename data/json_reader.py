# Python program to read
# json file
import json
  
def platforms_data():
    f = open('platformer/data/platforms.json',)
    data = json.load(f)
    f.close()

    return data['platforms']