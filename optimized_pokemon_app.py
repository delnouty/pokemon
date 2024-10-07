
import requests
import random
import time
import pandas as pd
from PIL import Image
import streamlit as st

# Function to fetch Pokémon data with optional limit
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
                "abilities": [ability["ability"]["name"] for ability in data["abilities"]],
                "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
                "image_url": data["sprites"]["front_default"]
            }
            pokemon_data.append(pokemon_info)
        else:
            st.warning(f"Failed to fetch data for Pokémon ID {i}")
        time.sleep(0.1)  # Avoid hitting the API rate limit
    return pokemon_data

# Convert the Pokémon data into a DataFrame
def save_to_dataframe(pokemon_data):
    df = pd.json_normalize(pokemon_data)
    return df

# Select random Pokémon
def select_random_pokemon(pokemon_list, count=16):
    if count > len(pokemon_list):
        raise ValueError("Count cannot be greater than the number of Pokémon in the list")
    return random.sample(pokemon_list, count)

# Create a grid layout for Pokémon display
def create_pokemon_grid(pokemon_list):
    num_pokemon = len(pokemon_list)
    grid_size = int(num_pokemon**0.5) + (1 if int(num_pokemon**0.5)**2 < num_pokemon else 0)
    # Streamlit's st.columns to create the grid layout
    cols = st.columns(grid_size)
    for i, pokemon in enumerate(pokemon_list):
        with cols[i % grid_size]:
            st.image(pokemon["image_url"], caption=pokemon["name"], width=100)
            st.write(f"ID: {pokemon['id']}")

# Streamlit app structure
st.title("Pokémon Dashboard")

# Fetch Pokémon data with limit set in sidebar
limit = st.sidebar.slider("Select Pokémon Fetch Limit", 1, 200, 100)
pokemon_data = fetch_pokemon_data(limit)

# Save the data to a DataFrame and display in the sidebar
pokemon_df = save_to_dataframe(pokemon_data)
st.sidebar.write("Pokémon DataFrame")
st.sidebar.dataframe(pokemon_df)

# Select and display a random set of Pokémon in grid format
random_pokemon = select_random_pokemon(pokemon_data, count=16)
st.write("Randomly Selected Pokémon")
create_pokemon_grid(random_pokemon)
