import json
import os
import redis
from dotenv import load_dotenv
import time
from enum import Enum
import csv
import json
import os
import requests

# Constants
itemsUrl = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/items.json"
pokemonUrl = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/monsters.json"
pokemonMoves = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/skills.json"

dataFolder = "./data/"

def validateFolders():
    for folder in [dataFolder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

def main():
    validateFolders()
    # Get items
    items = requests.get(itemsUrl)
    with open(dataFolder + "items.json", "w") as itemsFile:
        itemsFile.write(items.text)

    # Get pokemon
    pokemon = requests.get(pokemonUrl)
    with open(dataFolder + "pokemon.json", "w") as pokemonFile:
        pokemonFile.write(pokemon.text)

    # Get pokemon moves
    moves = requests.get(pokemonMoves)
    with open(dataFolder + "moves.json", "w") as movesFile:
        movesFile.write(moves.text)

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
    MOVES = 3

def validateFolders():
    for folder in [dataFolder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

def populateRedis(jsonData, dataType):
    print("Starting populate")
    print('Values: ')
    print(redis_host)
    print(redis_port)
    for data in jsonData:
        if(dataType == DataTypes.ITEMS):
            redis_items_client.set(data['id'], json.dumps(data))
        elif(dataType == DataTypes.POKEMON):
            redis_pokemon_client.set(data['id'], json.dumps(data))
        elif(dataType == DataTypes.MOVES):
            redis_moves_client.set(data['id'], json.dumps(data))

        time.sleep(0.01)

def populate():
    with open(dataFolder+'items.json') as itemData:
        populateRedis(json.load(itemData), DataTypes.ITEMS)

    with open(dataFolder+'pokemon.json') as pokemonData:
        populateRedis(json.load(pokemonData), DataTypes.POKEMON)

    with open(dataFolder+'moves.json') as movesData:
        populateRedis(json.load(movesData), DataTypes.MOVES)

if __name__ == "__main__":
    main()