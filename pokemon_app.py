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
                "abilities": [ability["ability"]["name"] for ability in data["abilities"]],
                "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
                "image_url": data["sprites"]["front_default"]
            }
            pokemon_data.append(pokemon_info)
        else:
            print(f"Failed to fetch data for Pokémon ID {i}")
        time.sleep(0.1)  # Adding a delay to avoid hitting the API rate limit
    return pokemon_data

def save_to_dataframe(pokemon_data):
    # Normalize the abilities list to separate columns
    df = pd.json_normalize(pokemon_data)
    return df

def select_random_pokemon(pokemon_list, count=16):
    if count > len(pokemon_list):
        raise ValueError("Count cannot be greater than the number of Pokémon in the list")
    return random.sample(pokemon_list, count)

def create_pokemon_grid(pokemon_list):
    num_pokemon = len(pokemon_list)
    grid_size = int(num_pokemon**0.5) + (1 if int(num_pokemon**0.5)**2 < num_pokemon else 0)
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

def battle(pokemon1, pokemon2):
    st.write(f"\nBattle between {pokemon1['name']} and {pokemon2['name']}!")
    hp1 = pokemon1['stats']['hp']
    hp2 = pokemon2['stats']['hp']
    
    while hp1 > 0 and hp2 > 0:
        # Pokémon 1 attacks
        attack1 = pokemon1['stats']['attack']
        hp2 -= attack1
        st.write(f"{pokemon1['name']} attacks {pokemon2['name']} for {attack1} damage. {pokemon2['name']} has {hp2} HP left.")
        if hp2 <= 0:
            st.write(f"{pokemon2['name']} fainted! {pokemon1['name']} wins!")
            return pokemon1, hp1
        
        # Pokémon 2 attacks
        attack2 = pokemon2['stats']['attack']
        hp1 -= attack2
        st.write(f"{pokemon2['name']} attacks {pokemon1['name']} for {attack2} damage. {pokemon1['name']} has {hp1} HP left.")
        if hp1 <= 0:
            st.write(f"{pokemon1['name']} fainted! {pokemon2['name']} wins!")
            return pokemon2, hp2

def run_tournament(pokemon_list):
    round_number = 1
    while len(pokemon_list) > 1:
        st.write(f"\n--- Round {round_number} ---")
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
        # Update the grid image after each round
        grid_image = create_pokemon_grid(pokemon_list)
        st.image(grid_image, caption="Pokémon Grid")
    
    st.write("\n--- Tournament Winner ---")
    st.write(f"The winner is {pokemon_list[0]['name']}!")
    display_winner_with_fireworks(pokemon_list[0])

def display_winner_with_fireworks(winner):
    # Load the winner's image
    response = requests.get(winner["image_url"])
    if response.status_code == 200:
        winner_image = Image.open(requests.get(winner["image_url"], stream=True).raw)
        winner_image = winner_image.resize((256, 256))
        
        # Display the winner's image
        st.image(winner_image, caption=f"Congratulations {winner['name']}!", use_column_width=True)
        
        # Display fireworks effect using HTML and CSS
        st.markdown("""
        <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%;">
            <iframe src="https://giphy.com/embed/l0HlBO7eyXzSZkJri" width="100%" height="100%" style="position: absolute;" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write(f"Failed to fetch image for {winner['name']}")

def main():
    st.title("Pokémon Battle Simulator")
    
    # Fetch data for the first 100 Pokémon
    pokemon_data = fetch_pokemon_data(100)
    
    # Randomly select 16 Pokémon
    try:
        random_pokemon = select_random_pokemon(pokemon_data, 16)
        
        # Save data to DataFrame
        df = save_to_dataframe(random_pokemon)
        
        st.write("Selected Pokémon DataFrame:")
        st.dataframe(df[["name", "abilities"]])
        
        # Run the tournament
        run_tournament(random_pokemon)
    except ValueError as e:
        st.error(e)

if __name__ == "__main__":
    main()
