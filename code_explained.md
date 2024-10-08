# Tableau de Bord du Tournoi Pokémon

## Aperçu
Ce projet Python implémente un **Tableau de Bord du Tournoi Pokémon** interactif utilisant **Streamlit**. Il permet aux utilisateurs de récupérer des données sur les Pokémon depuis la PokéAPI, de les afficher dans une mise en page en grille et de simuler des combats entre des Pokémon sélectionnés au hasard. L'application permet également aux utilisateurs d'organiser un tournoi où les Pokémon s'affrontent jusqu'à ce qu'un gagnant soit déclaré.

### Bibliothèques Clés :
- **requests** : Pour effectuer des requêtes HTTP et récupérer des données depuis la PokéAPI.
- **random** : Pour la sélection aléatoire des Pokémon et le mélange durant le tournoi.
- **time** : Utilisé pour ajouter un petit délai entre les requêtes API afin de prévenir les limites de taux.
- **pandas** : Pour structurer et afficher les données des Pokémon dans un DataFrame.
- **PIL (Image)** : Pour manipuler et afficher les images des Pokémon.
- **Streamlit** : Le cadre utilisé pour créer l'application web interactive.

---

## Explication du Code

### 1. `fetch_pokemon_data(limit=100)`
   - **Objectif** : Récupère des données de la PokéAPI pour un nombre spécifié de Pokémon (jusqu'à 200).
   - **Détails** :
     - Parcourt les ID des Pokémon et récupère leurs détails (nom, capacités, statistiques et URL de l'image).
     - Met en œuvre une gestion des erreurs pour gérer les erreurs potentielles HTTP ou de réseau, affichant des avertissements dans l'application.
     - Utilise un cache pour éviter les requêtes redondantes si les données ont déjà été récupérées.

### 2. `save_to_dataframe(pokemon_data)`
   - **Objectif** : Convertit la liste de données Pokémon en un **DataFrame pandas**.
   - **Détails** :
     - Prend la liste des données Pokémon et la normalise dans un tableau structuré en utilisant `pandas.json_normalize`.
     - Ce DataFrame est ensuite affiché dans la barre latérale pour une visualisation facile.

### 3. `select_random_pokemon(pokemon_list, count=16)`
   - **Objectif** : Sélectionne aléatoirement un nombre spécifié de Pokémon parmi les données récupérées.
   - **Détails** :
     - Échantillonne aléatoirement des Pokémon de la liste en utilisant `random.sample`.
     - S'assure que le nombre ne dépasse pas celui des Pokémon disponibles.

### 4. `create_pokemon_grid(pokemon_list)`
   - **Objectif** : Affiche une grille d'images de Pokémon avec leurs noms et IDs.
   - **Détails** :
     - Calcule une taille de grille appropriée en fonction du nombre de Pokémon.
     - Utilise la fonctionnalité `st.columns` de Streamlit pour organiser les Pokémon dans une mise en page en grille soignée.

### 5. `battle(pokemon1, pokemon2)`
   - **Objectif** : Simule un combat entre deux Pokémon en fonction de leurs statistiques.
   - **Détails** :
     - Chaque Pokémon attaque à tour de rôle en fonction de sa statistique d'attaque, réduisant les PV de l'adversaire.
     - Affiche les dégâts infligés et les PV restants dans l'application, et déclare un gagnant lorsque l'un des Pokémon s'évanouit.

### 6. `run_tournament(pokemon_list)`
   - **Objectif** : Simule un tournoi à élimination parmi un groupe de Pokémon.
   - **Détails** :
     - Mélange aléatoirement les Pokémon et les associe pour les combats.
     - Poursuit le tournoi par rondes jusqu'à ce qu'il ne reste qu'un seul Pokémon.
     - Met à jour l'affichage après chaque ronde, montrant quels Pokémon avancent à l'étape suivante.

### 7. `display_winner_with_fireworks(winner)`
   - **Objectif** : Affiche le Pokémon gagnant accompagné d'une animation de feux d'artifice.
   - **Détails** :
     - Récupère et affiche l'image du Pokémon gagnant.
     - Utilise HTML et CSS pour intégrer une animation de feux d'artifice Giphy dans l'application afin de célébrer le gagnant.

---

## Structure de l'Application Streamlit

### 1. **Titre**
   - L'application commence par un titre : `"Tableau de Bord Pokémon"`, affiché à l'aide de `st.title`.

### 2. **Entrées de la Barre Latérale**
   - Un curseur est fourni dans la barre latérale pour permettre aux utilisateurs de sélectionner combien de Pokémon ils souhaitent récupérer depuis l'API (de 1 à 200).
   - Les données des Pokémon récupérées sont ensuite affichées sous forme de **DataFrame pandas** dans la barre latérale.

### 3. **Affichage Principal**
   - Un groupe de 16 Pokémon sélectionnés aléatoirement est affiché dans la section principale sous format grille.
   - Un bouton (`st.button("Lancer le Tournoi")`) permet aux utilisateurs de démarrer un tournoi Pokémon.

---

## Interactions Clés avec l'Utilisateur
1. **Récupérer des Données Pokémon** : 
   - Les utilisateurs définissent une limite à l'aide du curseur de la barre latérale, et l'application récupère les données Pokémon de la PokéAPI.
2. **Sélection Aléatoire de Pokémon** :
   - L'application sélectionne 16 Pokémon aléatoires parmi les données récupérées et les affiche dans une grille.
3. **Simuler un Tournoi** :
   - Les utilisateurs peuvent simuler un tournoi à élimination où les Pokémon sélectionnés s'affrontent jusqu'à ce qu'un gagnant soit déclaré.
4. **Célébration avec Feux d'Artifice** :
   - Le Pokémon gagnant est affiché avec une animation de feux d'artifice de félicitations.

---

## Comment Exécuter le Projet

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/your-username/pokemon-tournament-dashboard.git
