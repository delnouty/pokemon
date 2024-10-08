# Pokémon Dashboard

Voici le code source pour le tableau de bord Pokémon. Ce projet utilise Streamlit pour afficher des informations sur les Pokémon, simuler des combats et organiser des tournois.

## Code complet

```python
import requests
import random
import time
import pandas as pd
from PIL import Image
import streamlit as st

# Fonction pour récupérer les données des Pokémon, avec une limite optionnelle
@st.cache_data
def fetch_pokemon_data(limit=100):
    """
    Cette fonction récupère les données des Pokémon depuis l'API PokeAPI.
    Le paramètre `limit` permet de spécifier combien de Pokémon récupérer (par défaut : 100).
    Les informations récupérées incluent l'ID, le nom, les capacités, les statistiques et l'URL de l'image de chaque Pokémon.
    """
    pokemon_data = []
    for i in range(1, limit + 1):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}"
        try:
            # Requête pour obtenir les données du Pokémon
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # Structure les informations importantes pour chaque Pokémon
            pokemon_info = {
                "id": data["id"],
                "name": data["name"],
                "abilities": [ability["ability"]["name"] for ability in data["abilities"]],
                "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
                "image_url": data["sprites"]["front_default"]
            }
            pokemon_data.append(pokemon_info)
        except requests.exceptions.HTTPError as http_err:
            st.warning(f"Erreur HTTP pour le Pokémon ID {i}: {http_err}")
        except Exception as err:
            st.warning(f"Autre erreur pour le Pokémon ID {i}: {err}")
        # Pause pour éviter de dépasser la limite de requêtes de l'API
        time.sleep(0.1)
    return pokemon_data

# Fonction pour sauvegarder les données des Pokémon sous forme de DataFrame
def save_to_dataframe(pokemon_data):
    """
    Convertit la liste des informations des Pokémon en un DataFrame pandas pour une manipulation plus facile.
    """
    df = pd.json_normalize(pokemon_data)
    return df

# Fonction pour sélectionner un nombre aléatoire de Pokémon
def select_random_pokemon(pokemon_list, count=16):
    """
    Sélectionne aléatoirement un certain nombre de Pokémon à partir de la liste des Pokémon récupérés.
    Par défaut, cette fonction en sélectionne 16.
    """
    if count > len(pokemon_list):
        raise ValueError("Le nombre de Pokémon sélectionnés ne peut pas excéder le total disponible.")
    return random.sample(pokemon_list, count)

# Fonction pour créer une grille de Pokémon
def create_pokemon_grid(pokemon_list):
    """
    Affiche les Pokémon sous forme de grille à l'aide de la fonctionnalité `st.columns` de Streamlit.
    Chaque cellule de la grille contient l'image du Pokémon et son ID.
    """
    num_pokemon = len(pokemon_list)
    grid_size = int(num_pokemon**0.5) + (1 if int(num_pokemon**0.5)**2 < num_pokemon else 0)
    # Utilisation des colonnes Streamlit pour structurer la grille
    cols = st.columns(grid_size)
    for i, pokemon in enumerate(pokemon_list):
        with cols[i % grid_size]:
            st.image(pokemon["image_url"], caption=pokemon["name"], width=100)
            st.write(f"ID: {pokemon['id']}")

# Fonction pour simuler un combat entre deux Pokémon
def battle(pokemon1, pokemon2):
    """
    Simule un combat entre deux Pokémon.
    Les Pokémon attaquent tour à tour jusqu'à ce que l'un d'eux n'ait plus de points de vie (HP).
    """
    st.write(f"\nCombat entre {pokemon1['name']} et {pokemon2['name']}!")
    hp1 = pokemon1['stats']['hp']
    hp2 = pokemon2['stats']['hp']
    
    while hp1 > 0 and hp2 > 0:
        # Le Pokémon 1 attaque
        attack1 = pokemon1['stats']['attack']
        hp2 -= attack1
        st.write(f"{pokemon1['name']} attaque {pokemon2['name']} pour {attack1} points de dégâts. {pokemon2['name']} a {hp2} HP restants.")
        if hp2 <= 0:
            st.write(f"{pokemon2['name']} est KO ! {pokemon1['name']} gagne !")
            return pokemon1, hp1
        
        # Le Pokémon 2 attaque
        attack2 = pokemon2['stats']['attack']
        hp1 -= attack2
        st.write(f"{pokemon2['name']} attaque {pokemon1['name']} pour {attack2} points de dégâts. {pokemon1['name']} a {hp1} HP restants.")
        if hp1 <= 0:
            st.write(f"{pokemon1['name']} est KO ! {pokemon2['name']} gagne !")
            return pokemon2, hp2

# Fonction pour exécuter un tournoi entre Pokémon
def run_tournament(pokemon_list):
    """
    Organise un tournoi à élimination directe entre les Pokémon.
    À chaque tour, les Pokémon se battent deux par deux jusqu'à ce qu'il ne reste qu'un vainqueur.
    """
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
        # Mettre à jour la grille après chaque tour
        create_pokemon_grid(pokemon_list)
    
    st.write("\n--- Gagnant du tournoi ---")
    st.write(f"Le gagnant est {pokemon_list[0]['name']}!")
    display_winner_with_fireworks(pokemon_list[0])

# Fonction pour afficher des feux d'artifice pour le vainqueur
def display_winner_with_fireworks(winner):
    """
    Affiche l'image du Pokémon vainqueur avec un effet de feux d'artifice.
    Utilise des balises HTML et CSS pour afficher une animation.
    """
    # Récupère l'image du vainqueur
    response = requests.get(winner["image_url"])
    if response.status_code == 200:
        winner_image = Image.open(requests.get(winner["image_url"], stream=True).raw)
        winner_image = winner_image.resize((256, 256))
        
        # Affiche l'image du vainqueur
        st.image(winner_image, caption=f"Félicitations {winner['name']}!", use_column_width=True)
        
        # Effet de feux d'artifice
        st.markdown("""
        <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%;">
            <iframe src="https://giphy.com/embed/l0HlBO7eyXzSZkJri" width="100%" height="100%" style="position: absolute;" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write(f"Impossible de récupérer l'image pour {winner['name']}")

# Structure de l'application Streamlit
st.title("Pokémon Dashboard")

# Récupération des données des Pokémon avec une limite définie par l'utilisateur dans la barre latérale
limit = st.sidebar.slider("Sélectionnez la limite de Pokémon à récupérer", 1, 200, 16)
pokemon_data = fetch_pokemon_data(limit)

# Sauvegarde des données dans un DataFrame et affichage dans la barre latérale
pokemon_df = save_to_dataframe(pokemon_data)
st.sidebar.write("Données des Pokémon")
st.sidebar.dataframe(pokemon_df)

# Sélection et affichage de Pokémon aléatoires dans une grille
random_pokemon = select_random_pokemon(pokemon_data, count=16)
st.write("Pokémon sélectionnés aléatoirement")
create_pokemon_grid(random_pokemon)

# Lancement d'un tournoi entre les Pokémon sélectionnés
if st.button("Lancer le tournoi"):
    run_tournament(random_pokemon)
