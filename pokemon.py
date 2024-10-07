import requests
import pandas as pd
import random

def fetch_pokemon_data(limit=50):
    pokemon_data = []
    for i in range(1, limit + 1):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemon_info = {
                "id": data["id"],
                "name": data["name"],
                "base_experience": data["base_experience"],
                "height": data["height"],
                "weight": data["weight"],
                "abilities": [ability["ability"]["name"] for ability in data["abilities"]],
                "types": [type_["type"]["name"] for type_ in data["types"]],
                "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
            }
            pokemon_data.append(pokemon_info)
        else:
            print(f"Failed to fetch data for Pokémon ID {i}")
    return pokemon_data

def save_to_dataframe(pokemon_data):
    df = pd.json_normalize(pokemon_data)
    return df

def select_random_pokemon(pokemon_list, count=16):
    return random.sample(pokemon_list, count)

def battle(pokemon1, pokemon2):
    print(f"\nBattle between {pokemon1['name']} and {pokemon2['name']}!")
    hp1 = pokemon1['stats']['hp']
    hp2 = pokemon2['stats']['hp']
    
    while hp1 > 0 and hp2 > 0:
        # Pokémon 1 attacks
        attack1 = pokemon1['stats']['attack']
        hp2 -= attack1
        print(f"{pokemon1['name']} attacks {pokemon2['name']} for {attack1} damage. {pokemon2['name']} has {hp2} HP left.")
        if hp2 <= 0:
            print(f"{pokemon2['name']} fainted! {pokemon1['name']} wins!")
            return pokemon1, hp1
        
        # Pokémon 2 attacks
        attack2 = pokemon2['stats']['attack']
        hp1 -= attack2
        print(f"{pokemon2['name']} attacks {pokemon1['name']} for {attack2} damage. {pokemon1['name']} has {hp1} HP left.")
        if hp1 <= 0:
            print(f"{pokemon1['name']} fainted! {pokemon2['name']} wins!")
            return pokemon2, hp2

def run_tournament(pokemon_list):
    round_number = 1
    while len(pokemon_list) > 1:
        print(f"\n--- Round {round_number} ---")
        next_round = []
        random.shuffle(pokemon_list)
        for i in range(0, len(pokemon_list), 2):
            if i + 1 < len(pokemon_list):
                winner, remaining_hp = battle(pokemon_list[i], pokemon_list[i + 1])
                next_round.append(winner)
            else:
                next_round.append(pokemon_list[i])
        pokemon_list = next_round
        round_number += 1
    
    print("\n--- Tournament Winner ---")
    print(f"The winner is {pokemon_list[0]['name']}!")

def main():
    # Fetch data for the first 100 Pokémon
    pokemon_data = fetch_pokemon_data(100)
    
    # Save data to DataFrame
    df = save_to_dataframe(pokemon_data)
    
    # Randomly select 16 Pokémon
    random_pokemon = select_random_pokemon(pokemon_data, 16)
    
    # Run the tournament
    run_tournament(random_pokemon)

if __name__ == "__main__":
    main()