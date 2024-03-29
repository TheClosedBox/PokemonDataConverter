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

def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    return False

def main():
    validate_folders()
    if not file_exists(itemsFile):
        items = requests.get(itemsUrl)
        with open(itemsFile, "w") as itemPath:
            json.dump(items.json(), itemPath)
            itemPath.write(items.text)
    if not file_exists(monstersFile):
        pokemon = requests.get(monstersUrl)
        with open(monstersFile, "w") as pokemonPath:
            json.dump(pokemon.json(), pokemonPath)
    if not file_exists(skillsFile):
        moves = requests.get(skillsUrl)
        with open(skillsFile, "w") as movePath:
            json.dump(moves.json(), movePath)
    extract_abilities()
    extract_locations()
    populate()

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")

class DataTypes(Enum):
    ITEMS = 1
    POKEMON = 2
    MOVES = 3
    ABILITIES = 4
    LOCATIONS = 5

redis_pokemon_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=DataTypes.POKEMON.value)
redis_items_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=DataTypes.ITEMS.value)
redis_moves_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=DataTypes.MOVES.value)
redis_abilities_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=DataTypes.ABILITIES.value)
redis_locations_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True, db=DataTypes.LOCATIONS.value)

def populate_redis(json_data, data_type):
    for data in json_data:
        if(data_type == DataTypes.ITEMS):
            redis_items_client.set(data['id'], json.dumps(data))
        elif(data_type == DataTypes.POKEMON):
            redis_pokemon_client.set(data['id'], json.dumps(data))
        elif(data_type == DataTypes.MOVES):
            redis_moves_client.set(data['id'], json.dumps(data))
        elif(data_type == DataTypes.ABILITIES):
            redis_abilities_client.set(data['id'], json.dumps(data))
        elif(data_type == DataTypes.LOCATIONS):
            redis_locations_client.set(data['location'], json.dumps(data))
        time.sleep(0.01)

def populate():
    with open(itemsFile) as itemData:
        populate_redis(json.load(itemData), DataTypes.ITEMS)
    with open(monstersFile) as monstersData:
        populate_redis(json.load(monstersData), DataTypes.POKEMON)
    with open(skillsFile) as skillsData:
        populate_redis(json.load(skillsData), DataTypes.MOVES)
    with open(abilitiesFile) as abilitiesData:
        populate_redis(json.load(abilitiesData), DataTypes.ABILITIES)
    with open(locationsFile) as locationsData:
        populate_redis(json.load(locationsData), DataTypes.LOCATIONS)
    
def extract_abilities():
    with open(monstersFile, "r") as pokemonData:
        pokemon = json.load(pokemonData)
        abilities = []
        for data in pokemon:
            for ability in data['abilities']:
                if ability not in abilities:
                    abilities.append(ability)
        with open(abilitiesFile, "w") as abilitiesData:
            json.dump(abilities, abilitiesData)

def extract_locations():
    with open(monstersFile) as pokemonData:
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
        with open(locationsFile, "w") as locationsData:
            json.dump(locations, locationsData)

if __name__ == "__main__":
    main()