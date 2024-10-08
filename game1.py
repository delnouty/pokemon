import requests
import random

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

# Fonction pour récupérer les données d'un Pokémon via son ID
def get_pokemon_data(pokemon_id):
    try:
        response = requests.get(f"{POKEAPI_URL}{pokemon_id}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données du Pokémon avec l'ID {pokemon_id}: {e}")
        return None

def get_stat(pokemon, stat_name):
    return next(stat['base_stat'] for stat in pokemon['stats'] if stat['stat']['name'] == stat_name)

def simulate_battle(pokemon1, pokemon2):
    # Récupérer toutes les statistiques importantes
    stats = ['attack', 'defense', 'hp', 'special-attack', 'special-defense']
    
    score1 = sum(get_stat(pokemon1, stat) for stat in stats)
    score2 = sum(get_stat(pokemon2, stat) for stat in stats)

    print(f"Combat entre {pokemon1['name']} et {pokemon2['name']}: {score1} vs {score2}")

    # Comparer les scores
    if score1 == score2:
        # Si les scores sont égaux, comparer la vitesse
        speed1 = get_stat(pokemon1, 'speed')
        speed2 = get_stat(pokemon2, 'speed')
        print(f"Scores égaux, comparaison des vitesses: {speed1} vs {speed2}")
        return pokemon1 if speed1 > speed2 else pokemon2
    else:
        return pokemon1 if score1 > score2 else pokemon2

# Fonction pour choisir 16 Pokémon aléatoires
def choose_random_pokemon(n=16):
    pokemon_list = []
    while len(pokemon_list) < n:
        pokemon_id = random.randint(1, 898)  # Il y a 898 Pokémon dans PokeAPI (génération 1 à 8)
        pokemon_data = get_pokemon_data(pokemon_id)
        if pokemon_data:
            pokemon_list.append(pokemon_data)
            print(f"Ajouté {pokemon_data['name']} au tournoi.")
    return pokemon_list

# Fonction pour simuler un tournoi
def simulate_tournament():
    # Sélectionner 16 Pokémon aléatoirement
    participants = choose_random_pokemon(16)

    round_number = 1
    while len(participants) > 1:
        print(f"--- Tour {round_number} ---")
        next_round = []
        
        # Simuler les combats en paires
        for i in range(0, len(participants), 2):
            winner = simulate_battle(participants[i], participants[i+1])
            next_round.append(winner)
        
        participants = next_round
        round_number += 1

    # Le dernier Pokémon est le champion
    champion = participants[0]
    print(f"Le champion du tournoi est {champion['name']} !")

# Lancer le tournoi
simulate_tournament()
