# Segment-tree-representation

Ce programme Python génère une visualisation animée d'un arbre de segments, une structure de données efficace pour les requêtes d'intervalles (sommes, minimums, etc.). L'animation illustre la construction de l'arbre et son utilisation pour calculer des sommes sur des intervalles spécifiés.

## Fonctionnalités

* **Visualisation interactive :** Représentation graphique des nœuds et des connexions parent-enfant.
* **Animation progressive :** Construction étape par étape de l'arbre.
* **Calcul de somme d'intervalle :** Calcul et affichage de la somme des éléments dans un intervalle donné.
* **Sauvegarde d'image :** Capture et sauvegarde de l'image finale de l'arbre.

## Techniques Employées

* **Langage :** Python
* **Bibliothèques :**
    * Pygame (interface graphique)
    * Colormath (gestion des couleurs)
    * Math (calculs mathématiques)
    * OrderedDict (stockage ordonné des nœuds)
    * Pillow (sauvegarde d'image)
* **Structure de données :** Arbre de segments implémenté avec un dictionnaire Python.

## Utilisation

1.  **Installation des dépendances :**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Exécution du programme :**

    ```bash
    python main.py
    ```

3.  **Entrées utilisateur :**

    * Taille du tableau
    * Valeurs des éléments du tableau
    * Indices de début et de fin de l'intervalle
    * Nom du fichier de sauvegarde

## Limitations

* Visualisation limitée à un nombre raisonnable de nœuds.
* Pas de support pour les modifications dynamiques du tableau.
