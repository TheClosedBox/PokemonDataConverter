import csv
import json
import os
import requests

# Constants
itemsUrl = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/items.json"
pokemonUrl = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/monsters.json"
pokemonMoves = "https://raw.githubusercontent.com/Team-Porygon-PokeMMO/PokeMMO-Data/main/skills.json"

outputFolder = "./output/"
dataFolder = "./data/"

def validateFolders():
    for folder in [outputFolder, dataFolder]:
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

if __name__ == "__main__":
    main()