# Databricks notebook source
# MAGIC %md
# MAGIC Ce projet analyse les flux de streaming Spotify pour identifier les tendances, les artistes les plus populaires et le profil audio des hits. L’objectif est de démontrer la capacité à exploiter des données brutes, à réaliser de la data cleaning, une analyse exploratoire, et à produire des tableaux de bord exploitables.

# COMMAND ----------

# -------------------------------------------
# Projet : Analyse Spotify Popularity Songs - Databricks
# Objectif : analyser la popularité Spotify (streams, saisonnalité, audio)
# -------------------------------------------

from pyspark.sql.functions import col, regexp_replace, format_number, when  # Imports Spark utiles
from pyspark.sql.types import DoubleType
import re

# Nettoyage des noms de colonne (enlève caractères spéciaux)
def clean_col_name(name):                                        # Définit une fonction de nettoyage des colonnes
    return re.sub(r"[ \(\)\{\}\[\],;\'\"\n\t\-=\+]", "_", name)  # Remplace tous les caractères non alphanumériques par '_'

# Chargement de la table source Databricks
table_name = "workspace.default.popular_spotify_songs"           # Spécifie le nom de ta table
df = spark.table(table_name)                                     # Charge la table en DataFrame

clean_cols = [clean_col_name(c) for c in df.columns]             # Applique la fonction à chaque colonne pour avoir des noms propres
df_clean = df.toDF(*clean_cols)                                  # Renomme les colonnes nettoyées dans la DataFrame
print("Colonnes nettoyées :", df_clean.columns)                  # Affiche les nouveaux noms de colonnes

# Nettoyage et conversion de la colonne 'streams'
df_clean = df_clean.withColumn(
    "streams",
    regexp_replace("streams", "[^0-9.]", "")                     # Retire des caractères parasites
).withColumn(
    "streams", col("streams").cast(DoubleType())                 # Cast la colonne streams en float
).na.drop(subset=["streams"])                                    # Retire les titres où le stream est vide

# Ajoute colonne 'streams_millions' (plus lisible pour les visus)
df_clean = df_clean.withColumn("streams_millions", format_number(col("streams")/1e6, 1)) 

# Suppression spécifique d'artistes outliers qui biaisent les analyses
artist_col = next((c for c in df_clean.columns if "artist" in c), None)  # Cherche la colonne artiste automatiquement
if artist_col:
    for bad in ["Edison Lighthouse", "Carin Leon, Grupo Frontera"]:      # Liste des artistes à enlever
        df_clean = df_clean.filter(col(artist_col) != bad)

track_col = next((c for c in df_clean.columns if "track" in c), None)    # Cherche la colonne track automatiquement

# Création du label de mois avec numéro pour garantir le bon ordre X dans les visuels
df_clean = df_clean.withColumn(
    "released_month_full_label",
    when(col("released_month") == 1, "01-Janvier")
    .when(col("released_month") == 2, "02-Février")
    .when(col("released_month") == 3, "03-Mars")
    .when(col("released_month") == 4, "04-Avril")
    .when(col("released_month") == 5, "05-Mai")
    .when(col("released_month") == 6, "06-Juin")
    .when(col("released_month") == 7, "07-Juillet")
    .when(col("released_month") == 8, "08-Août")
    .when(col("released_month") == 9, "09-Septembre")
    .when(col("released_month") == 10, "10-Octobre")
    .when(col("released_month") == 11, "11-Novembre")
    .otherwise("12-Décembre")
)

# Statistiques sur les streams pour analyse basique et détection outlier
print("Statistiques descriptives sur les streams :")
df_clean.describe("streams").show()

# Bar chart : top 10 artistes par streams cumulés
if artist_col:
    top_artists = df_clean.groupBy(artist_col)\
        .sum("streams")\
        .orderBy(col("sum(streams)").desc())\
        .limit(10)\
        .withColumn("streams_millions", format_number(col("sum(streams)")/1e6, 1))
    print("Top 10 artistes par streams cumulés")
    display(top_artists.select(artist_col, "streams_millions")) # Affiche un graphique du top 10 artistes

# Distribution : nombre de streams par titre (pour visualiser la dispersion des succès)
print("Nombre de streams par titre")
display(df_clean.select(artist_col, track_col, "streams_millions"))

# Evolution des streams cumulés par année (visualisation tendance globale Spotify)
if "released_year" in df_clean.columns:
    yearly_streams = df_clean.groupBy("released_year").sum("streams").orderBy("released_year")
    print("Evolution des streams cumulés par année")
    display(yearly_streams)

# Histogramme : nombre de morceaux sortis par année
df_year = df_clean.groupBy("released_year").count().orderBy("released_year")
print("Nombre de morceaux sortis par année")
display(df_year)

# Bar chart : nombre de morceaux sortis par mois en ordre calendrier (clé pour l'axe X !)
df_month_full_label = df_clean.groupBy("released_month_full_label").count().orderBy("released_month_full_label")
print("Nombre de morceaux sortis par mois")
display(df_month_full_label)

# Historique : combien de morceaux par jour du mois (voir effet calendrier)
df_day = df_clean.groupBy("released_day").count().orderBy("released_day")
print("Nombre de morceaux sortis par jour du mois")
display(df_day)

# Profils audio des top 5 artistes les plus streamés (comparatif des grandes dimensions musicales Spotify)
audio_features_keywords = ['danceability', 'energy', 'acousticness',
                          'instrumentalness', 'liveness', 'valence']
audio_cols = [c for c in df_clean.columns if any(c.startswith(k) for k in audio_features_keywords)]
if artist_col and audio_cols and "top_artists" in locals():
    top5_rows = top_artists.select(artist_col).limit(5).collect()
    top5_artists = [row[artist_col] for row in top5_rows]
    df_top5_audio = df_clean.filter(col(artist_col).isin(top5_artists)).groupBy(artist_col).avg(*audio_cols)
    print(f"Profils audio des top 5 artistes les plus streamés : {', '.join(top5_artists)}")
    display(df_top5_audio)

# Segmentation : proportion des titres à très fort succès (> 70M streams)
threshold = 70000000
df_final = df_clean.withColumn("streams_high", (col("streams") >= threshold).cast("integer"))
if artist_col:
    pop_dist = df_final.groupBy("streams_high").count()
    print(f"Proportion des titres à très fort succès (> {threshold:,} streams) :")
    print(f"{pop_dist.filter(col('streams_high') == 1).collect()[0]['count']:,}/{pop_dist.filter(col('streams_high') == 0).collect()[0]['count']:,}")
    display(pop_dist)

# Sauvegarde sous forme de Delta Table propres, pour BI/présentation/re-use
df_final.write.option("mergeSchema", "true").mode("overwrite").saveAsTable("spotify_streams_analysis_final")

print("✅ Analyse terminée et documentée. Colonnes X garanties en ordre calendaire.")
