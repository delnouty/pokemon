# Tournoi Pokémon

Bienvenue dans **Tournoi Pokémon**, une application Python interactive qui simule un tournoi épique entre 16 Pokémon sélectionnés aléatoirement en utilisant les données de l'[API PokeAPI](https://pokeapi.co/). Grâce à une interface intuitive créée avec Streamlit, suivez le parcours de vos Pokémon favoris jusqu'à la désignation du champion ultime.

## Table des Matières

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
  - [Prérequis](#prérequis)
  - [Étapes d'Installation](#étapes-dinstallation)
- [Utilisation](#utilisation)
- [Technologies Utilisées](#technologies-utilisées)
- [Gestion des Erreurs](#gestion-des-erreurs)
- [Contribution](#contribution)
- [Licence](#licence)

## Présentation

**Tournoi Pokémon** est un programme Python qui simule un tournoi entre 16 Pokémon sélectionnés aléatoirement via la PokeAPI. Le programme :

- Sélectionne aléatoirement 16 Pokémon.
- Simule des combats jusqu'à la désignation du champion.
- Affiche les résultats avec des visuels attractifs.
- Gère les erreurs de requêtes API et autres problèmes automatiquement.

## Fonctionnalités

- **Sélection Aléatoire** : Choix aléatoire de 16 Pokémon parmi une large base de données.
- **Simulation de Tournoi** : Tournoi éliminatoire avec combats automatisés.
- **Interface Interactive** : Suivez les combats et le tournoi à travers une interface Streamlit.
- **Visualisation des Pokémon** : Affichage des images des Pokémon et des effets visuels pour le gagnant.
- **Gestion des Erreurs** : Notifications d'erreurs lors des requêtes API ou d'autres problèmes.

## Installation

### Prérequis

- **Python 3.7+**
- **pip** (gestionnaire de paquets Python)

### Étapes d'Installation

1. **Cloner le dépôt** :
    ```bash
    git clone https://github.com/votre-utilisateur/tournoi-pokemon.git
    cd tournoi-pokemon
    ```

2. **Créer un environnement virtuel** (optionnel mais recommandé) :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    ```

3. **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```
    Si le fichier `requirements.txt` n'est pas fourni, installez manuellement les paquets nécessaires :
    ```bash
    pip install requests pandas Pillow streamlit
    ```

## Utilisation

1. **Lancer l'application** :
    ```bash
    streamlit run app.py
    ```
    Remplacez `app.py` par le nom de votre fichier principal si nécessaire.

2. **Interactions dans l'interface** :
    - **Sélection du nombre de Pokémon** : Utilisez le slider pour choisir combien de Pokémon récupérer (par défaut 16).
    - **Visualisation des données** : Consultez le tableau des Pokémon récupérés dans la barre latérale.
    - **Affichage des Pokémon** : La grille principale affiche les Pokémon sélectionnés avec leurs images et identifiants.
    - **Lancer le Tournoi** : Cliquez sur le bouton "Run Tournament" pour démarrer la simulation. Suivez les combats jusqu'au champion !

## Technologies Utilisées

- **Python** : Langage principal.
- **Streamlit** : Interface utilisateur interactive.
- **Requests** : Pour les requêtes HTTP vers l'API PokeAPI.
- **Pandas** : Manipulation et affichage des données.
- **Pillow** : Traitement des images des Pokémon.
- **Random** : Sélection aléatoire des Pokémon.
- **Time** : Gestion des délais entre les requêtes API.

## Gestion des Erreurs

Le programme est conçu pour gérer les erreurs liées aux requêtes API et aux limitations de l'API :

- **Erreurs HTTP** : Avertissement si une requête pour un Pokémon échoue.
- **Limitation de Taux** : Délai de 0,1 seconde entre les requêtes pour éviter de dépasser les limites de l'API.
- **Gestion Générale des Erreurs** : Capture et notification des autres erreurs.

## Contribution

Les contributions sont encouragées ! Pour participer :

1. Forker le dépôt.
2. Créer une nouvelle branche pour votre fonctionnalité :
    ```bash
    git checkout -b feature/nom-de-la-fonctionnalité
    ```
3. Committer vos modifications :
    ```bash
    git commit -m "Ajout de la fonctionnalité ..."
    ```
4. Pousser la branche sur GitHub :
    ```bash
    git push origin feature/nom-de-la-fonctionnalité
    ```
5. Ouvrir une Pull Request.

Assurez-vous de respecter les standards de codage et d'ajouter des tests si possible.

## Licence

Ce projet est sous licence MIT.
