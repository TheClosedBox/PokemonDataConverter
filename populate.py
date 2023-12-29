import csv
import json
import os
import redis
from dotenv import load_dotenv

outputFolder = "./output/"
dataFolder = "./data/"

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def validateFolders():
    for folder in [outputFolder, dataFolder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

def populateRedis(jsonData):
    for pokemon in jsonData:
        redis_client.set(pokemon['pokedex_number'], json.dumps(pokemon))

def main():
    validateFolders()

    with open(outputFolder+'exp_growth.json') as pokemonData:
        populateRedis(pokemonData)

if __name__ == "__main__":
    main()