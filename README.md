# Projet : Analyse de la Popularité des Morceaux Spotify sur Databricks

**`spotify-popularity-analysis`**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Databricks](https://img.shields.io/badge/Made%20with-Databricks-orange.svg)](https://www.databricks.com/)
[![PySpark](https://img.shields.io/badge/Language-PySpark-blueviolet.svg)](https://spark.apache.org/docs/latest/api/python/)

## 🚀 Vue d'Ensemble du Projet

Ce projet **Databricks** fournit une solution complète pour analyser la popularité des morceaux sur Spotify. En exploitant la puissance de PySpark, il nettoie des données brutes, enrichit les informations avec des métriques clés (comme les streams en millions) et génère des insights visuels exploitables sur les tendances de popularité, la saisonnalité des sorties et les profils audio des artistes.

L'objectif principal est de transformer des données complexes en **informations stratégiques claires** pour comprendre ce qui rend un morceau populaire, identifier les artistes majeurs et déceler des patterns de succès sur la plateforme Spotify.

## ✨ Fonctionnalités Clés

*   **Nettoyage de Données Robuste** : Automatisation du nettoyage des noms de colonnes et standardisation de la colonne `streams`.
*   **Enrichissement des Données** : Ajout de métriques lisibles comme `streams_millions` et de labels de mois ordonnés pour des visualisations précises.
*   **Détection et Gestion des Outliers** : Identification et suppression d'artistes qui pourraient fausser les analyses.
*   **Analyses Exploratoires Approfondies** :
    *   Top 10 des artistes par streams cumulés.
    *   Distribution des streams par titre.
    *   Tendances annuelles et mensuelles des sorties de morceaux.
    *   Analyse de la répartition des sorties par jour du mois.
    *   Profils audio comparatifs des top artistes (danse, énergie, acoustique, etc.).
*   **Segmentation Stratégique** : Identification des titres à "très fort succès" (> 70 millions de streams).
*   **Output Prêt pour la BI** : Sauvegarde des résultats nettoyés et enrichis dans une Delta Lake Table optimisée pour des dashboards BI et des analyses ultérieures.

## 🎯 Pourquoi ce Projet ?

Dans l'industrie musicale actuelle, comprendre les dynamiques de popularité est crucial. Ce projet offre :

*   **Gain de Temps** : Automatise un processus complexe de préparation et d'analyse de données.
*   **Insights Précis** : Fournit des visualisations ordonnées et des statistiques fiables.
*   **Évolutivité** : Conçu sur Databricks avec PySpark, il gère efficacement de très grands volumes de données Spotify.
*   **Réutilisabilité** : La Delta Table finale est une source de données propre et structurée, prête à être consommée par d'autres applications ou outils de Business Intelligence.

## 🛠️ Technologies Utilisées

*   **Databricks** : Environnement de développement et d'exécution cloud-native pour l'ingénierie et la science des données.
*   **Apache Spark (PySpark)** : Moteur d'analyse de données distribué, utilisé pour le traitement et la transformation des DataFrames.
*   **Delta Lake** : Format de stockage open source qui apporte la fiabilité des transactions ACID à Data Lakes.

## 📊 Exemple de Visualisation

Voici un aperçu du type d'insights générés par ce notebook, illustrant par exemple l'évolution des streams cumulés par année :
*Exemple de Bar Chart généré par Databricks montrant le Top 10 des artistes par streams cumulés.*

*Exemple de visualisation de l'évolution des streams cumulés par année, illustrant une tendance globale.*

## 🚀 Comment Lancer le Projet

### Prérequis

*   Accès à un environnement **Databricks**.
*   Une table source nommée `workspace.default.popular_spotify_songs` contenant les données brutes des morceaux Spotify.
    *   *Structure attendue de la table source :* Colonnes telles que `streams`, `artist_name`, `track_name`, `released_year`, `released_month`, `released_day` et diverses caractéristiques audio (`danceability`, `energy`, etc.).

### Étapes

1.  **Importer le Notebook** : Téléchargez le fichier `.py` ou `.ipynb` de ce dépôt et importez-le dans votre workspace Databricks.
2.  **Attacher à un Cluster** : Attachez le notebook à un cluster Databricks configuré avec Spark.
3.  **Exécuter Toutes les Cellules** : Lancez toutes les cellules du notebook. Le script se chargera de :
    *   Charger les données.
    *   Nettoyer et transformer les colonnes.
    *   Effectuer les analyses et afficher les visualisations directement dans le notebook.
    *   Sauvegarder la table `spotify_streams_analysis_final` dans votre Delta Lake par défaut.

## 📈 Résultats et Output

Le script produit plusieurs visualisations interactives directement dans l'environnement Databricks (utilisant la commande `display()`).

La sortie finale est une table **Delta Lake** appelée `spotify_streams_analysis_final`, prête à être utilisée pour :

*   La création de dashboards interactifs avec des outils comme Tableau, Power BI, ou Databricks SQL Analytics.
*   Des analyses prédictives ou du Machine Learning sur la popularité des chansons.
*   Des rapports automatisés sur les tendances musicales.

## 🤝 Contribution

Les contributions sont les bienvenues ! Si vous avez des suggestions d'amélioration ou de nouvelles fonctionnalités :

1.  Forkez ce dépôt.
2.  Créez une nouvelle branche (`git checkout -b feature/AmazingFeature`).
3.  Commitez vos modifications (`git commit -m 'Add some AmazingFeature'`).
4.  Poussez la branche (`git push origin feature/AmazingFeature`).
5.  Ouvrez une Pull Request.

## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
