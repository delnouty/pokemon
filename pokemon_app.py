import requests
import random
import time
import pandas as pd
from PIL import Image
import streamlit as st

def fetch_pokemon_data(limit=100):
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
                "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
                "image_url": data["sprites"]["front_default"]
            }
            pokemon_data.append(pokemon_info)
        else:
            print(f"Failed to fetch data for Pokémon ID {i}")
        time.sleep(0.1)  # Adding a delay to avoid hitting the API rate limit
    return pokemon_data

def save_to_dataframe(pokemon_data):
    # Normalize the stats dictionary to separate columns
    df = pd.json_normalize(pokemon_data)
    return df

def select_random_pokemon(pokemon_list, count=16):
    if count > len(pokemon_list):
        raise ValueError("Count cannot be greater than the number of Pokémon in the list")
    return random.sample(pokemon_list, count)

def create_pokemon_grid(pokemon_list, grid_size=4):
    cell_size = 64  # Size of each cell in the grid
    grid_image = Image.new('RGB', (grid_size * cell_size, grid_size * cell_size))
    
    for idx, pokemon in enumerate(pokemon_list):
        response = requests.get(pokemon["image_url"])
        if response.status_code == 200:
            pokemon_image = Image.open(requests.get(pokemon["image_url"], stream=True).raw)
            pokemon_image = pokemon_image.resize((cell_size, cell_size))
            x = (idx % grid_size) * cell_size
            y = (idx // grid_size) * cell_size
            grid_image.paste(pokemon_image, (x, y))
        else:
            print(f"Failed to fetch image for {pokemon['name']}")
    
    return grid_image

def battle_round(pokemon_list):
    # Simulate a battle round (this is just a placeholder for actual battle logic)
    st.write("Battle round!")
    # Display the grid after each round
    grid_image = create_pokemon_grid(pokemon_list)
    st.image(grid_image, caption="Pokémon Grid")

def main():
    st.title("Pokémon Battle Simulator")
    
    # Fetch data for the first 100 Pokémon
    pokemon_data = fetch_pokemon_data(100)
    
    # Save data to DataFrame
    df = save_to_dataframe(pokemon_data)
    
    st.write("Pokémon DataFrame:")
    st.dataframe(df.head())
    
    # Randomly select 16 Pokémon
    try:
        random_pokemon = select_random_pokemon(pokemon_data, 16)
        st.write("Randomly selected Pokémon:")
        for pokemon in random_pokemon:
            st.write(pokemon["name"])
        
        # Simulate battle rounds and display the grid after each round
        for _ in range(3):  # Example: 3 battle rounds
            battle_round(random_pokemon)
    except ValueError as e:
        st.error(e)

if __name__ == "__main__":
    main()
