import json
import os
import redis
from dotenv import load_dotenv
import time
from enum import Enum
import json
import os
import requests
import io
import shutil

# Constants
itemsUrl = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/items.json"
monstersUrl = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/monsters.json"
skillsUrl = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/skills.json"

dataFolder = "./data/"

itemsFile = dataFolder + "items.json"
monstersFile = dataFolder + "monsters.json"
skillsFile = dataFolder + "skills.json"
abilitiesFile = dataFolder + "abilities.json"
locationsFile = dataFolder + "locations.json"

def validate_folders():
    for folder in [dataFolder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            return
        shutil.rmtree(folder)
        os.makedirs(folder)

def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    return False

def main():
    validate_folders()
    if not file_exists(itemsFile):
        items = requests.get(itemsUrl)
        with open(itemsFile, "w", encoding="utf-8") as itemPath:
            itemPath.write(items.text)
    if not file_exists(monstersFile):
        pokemon = requests.get(monstersUrl)
        with open(monstersFile, "w", encoding="utf-8") as pokemonPath:
            pokemonPath.write(pokemon.text)
    if not file_exists(skillsFile):
        moves = requests.get(skillsUrl)
        with open(skillsFile, "w", encoding="utf-8") as movePath:
            movePath.write(moves.text)
    extract_abilities()
    extract_locations()
    populate()

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")
redis_pokemon_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=0)
redis_items_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=1)
redis_moves_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=2)

class DataTypes(Enum):
    ITEMS = 1
    POKEMON = 2
    MOVES = 3,
    ABILITIES = 4,
    LOCATIONS = 5

def populate_edis(json_data, data_type):
    for data in json_data:
        if(data_type == DataTypes.ITEMS):
            redis_items_client.set(data['id'], json.dumps(data))
        elif(data_type == DataTypes.POKEMON):
            redis_pokemon_client.set(data['id'], json.dumps(data))
        elif(data_type == DataTypes.MOVES):
            redis_moves_client.set(data['id'], json.dumps(data))
        elif(data_type == DataTypes.ABILITIES):
            redis_moves_client.set(data['id'], json.dumps(data))
        elif(data_type == DataTypes.LOCATIONS):
            redis_moves_client.set(data['location'], json.dumps(data))
        time.sleep(0.01)

def populate():
    with open(itemsFile,"r", encoding="utf-8") as itemData:
        populate_edis(json.load(itemData), DataTypes.ITEMS)
    with open(monstersFile,"r", encoding="utf-8") as monstersData:
        populate_edis(json.load(monstersData), DataTypes.POKEMON)
    with open(skillsFile,"r", encoding="utf-8") as skillsData:
        populate_edis(json.load(skillsData), DataTypes.MOVES)
    with open(abilitiesFile,"r", encoding="utf-8") as abilitiesData:
        populate_edis(json.load(abilitiesData), DataTypes.ABILITIES)
    with open(locationsFile,"r", encoding="utf-8") as locationsData:
        populate_edis(json.load(locationsData), DataTypes.LOCATIONS)
    
def extract_abilities():
    with open(monstersFile, "r", encoding="utf-8") as pokemonData:
        pokemon = json.load(pokemonData)
        abilities = []
        for data in pokemon:
            for ability in data['abilities']:
                if ability not in abilities:
                    abilities.append(ability)
        with open(abilitiesFile, "w+", encoding="utf-8") as abilitiesData:
            abilities.sort(key=lambda x: x['name'])
            json.dump(abilities, abilitiesData)

def extract_locations():
    with open(monstersFile, "r", encoding="utf-8") as pokemonData:
        pokemon = json.load(pokemonData)
        locations = []
        for data in pokemon:
            for location in data['locations']:
                new_location = {
                    "region_id": location['region_id'],
                    "region_name": location['region_name'],
                    "location": location['location'],
                }
                if new_location not in locations:
                    locations.append(new_location)
        with open(locationsFile, "w+", encoding="utf-8") as locationsData:
            locations.sort(key=lambda x: x['region_id'])
            json.dump(locations, locationsData)

if __name__ == "__main__":
    main()