import json
import os
import redis
from dotenv import load_dotenv
import time
from enum import Enum

dataFolder = "./data/"

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
        for data in jsonData:
            if(dataType == DataTypes.ITEMS):
                print('Inserting item: ' + data['id'])
                redis_items_client.set(data['id'], json.dumps(data))
            elif(dataType == DataTypes.POKEMON):
                print('Inserting pokemon: ' + data['id'])
                redis_pokemon_client.set(data['id'], json.dumps(data))
            elif(dataType == DataTypes.MOVES):
                print('Inserting move: ' + data['id'])
                redis_moves_client.set(data['id'], json.dumps(data))

            time.sleep(0.001)

def main():
    validateFolders()

    with open(dataFolder+'items.json') as itemData:
        populateRedis(json.load(itemData), DataTypes.ITEMS)

    with open(dataFolder+'pokemon.json') as pokemonData:
        populateRedis(json.load(pokemonData), DataTypes.POKEMON)

    with open(dataFolder+'moves.json') as movesData:
        populateRedis(json.load(movesData), DataTypes.MOVES)

if __name__ == "__main__":
    main()