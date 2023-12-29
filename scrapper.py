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

    with open(dataFolder+'pokemon.csv', newline='', encoding="utf-8") as csvfile:
        for header in open('data/headers.csv', newline='', encoding="utf-8"):
            headers = header.split(',')
    with open(dataFolder+'pokemon.csv', newline='', encoding="utf-8") as csvfile:
        pokemons = csv.reader(csvfile)
        pokemonsData = []
        for pokemon in pokemons:
            abilities = pokemon[0]
            vsBug = pokemon[1]
            vsDark = pokemon[2]
            vsDragon = pokemon[3]
            vsElectric = pokemon[4]
            vsFairy = pokemon[5]
            vsFight = pokemon[6]
            vsFire = pokemon[7]
            vsFlying = pokemon[8]
            vsGhost = pokemon[9]
            vsGrass = pokemon[10]
            vsGround = pokemon[11]
            vsIce = pokemon[12]
            vsNormal = pokemon[13]
            vsPoison = pokemon[14]
            vsPsychic = pokemon[15]
            vsRock = pokemon[16]
            vsSteel = pokemon[17]
            vsWater = pokemon[18]
            attack = pokemon[19]
            base_egg_steps = pokemon[20]
            base_happiness = pokemon[21]
            base_total = pokemon[22]
            capture_rate = pokemon[23]
            classfication = pokemon[24]
            defense = pokemon[25]
            experience_growth = pokemon[26]
            height_m = pokemon[27]
            hp = pokemon[28]
            name = pokemon[30]
            percentage_male = pokemon[31]
            pokedex_number = pokemon[32]
            sp_attack = pokemon[33]
            sp_defense = pokemon[34]
            speed = pokemon[35]
            type1 = pokemon[36]
            type2 = pokemon[37]
            weight_kg = pokemon[38]
            generation = pokemon[39]
            is_legendary = pokemon[40]

            # For exp porpuses
            pokemonExpData = {
                'name':name,
                'pokedex_number':pokedex_number,
                'experience_growth':experience_growth
            }
            
            pokemonsData.append(pokemonExpData)
        populateRedis(pokemonsData)

if __name__ == "__main__":
    main()