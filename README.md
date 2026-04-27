## Amazon — Analyse Exploratoire
J'ai travaillé sur un dataset de produits Amazon pour pratiquer l'analyse de données de bout en bout : nettoyage, exploration, visualisation et extraction d'insights business.
C'est un projet que j'ai réalisé pour monter en compétences sur pandas et matplotlib en partant de données réelles et un peu sales (prix en ₹ avec des virgules, catégories imbriquées, valeurs manquantes).

## Ce que j'ai fait

Nettoyage complet des colonnes prix, remises et notes
Extraction de la catégorie principale depuis la hiérarchie Amazon
Création d'un score de popularité maison : note × log(nb_avis)
3 visualisations exportées en PNG
2 fichiers CSV de résultats prêts à partager


## Outils utilisés

Python, pandas, numpy
matplotlib, seaborn


## Les 3 choses que j'ai trouvées

Les catégories tech (Electronics, Computers) dominent largement le catalogue — Amazon est avant tout une plateforme orientée high-tech
La remise médiane dépasse 40% — les vendeurs jouent clairement sur l'effet "bonne affaire" pour attirer les acheteurs
Note élevée ≠ produit populaire — un produit à 4,1★ avec 15 000 avis est bien plus visible qu'un 4,8★ avec 200 avis


## Lancer le projet
## bashpip install pandas numpy matplotlib seaborn
## python Amazon.py 
