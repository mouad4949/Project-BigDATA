import pandas as pd
import numpy as np

# 1. Charger les données (Simulons le chargement depuis votre JSON final)
df = pd.read_json("Data-Collection/final_data2.json")
# Pour l'exemple, créons un DataFrame fictif basé sur votre structure
#data = {
 #   'title': ['Paper A', 'Paper B', 'Paper C', 'Paper D'],
 #   'authors': ['Wang; Liu', 'Smith', 'Wang', 'Doe; Smith'],
 #   'date_pub': [2019, 2020, 2019, 2021],
  #  'journal': ['IEEE Trans', 'Nature', 'IEEE Trans', 'ACM'],
  #  'country': ['USA', 'UK', 'China', 'USA'],
  #  'quartile': ['Q1', 'Q1', 'Q2', 'Q3']
#}
#df = pd.DataFrame(data)

# --- A. CRÉATION DES DIMENSIONS (Les axes d'analyse) --- [cite: 126]

# 1. Dimension TEMPS (D_Temps)
d_temps = pd.DataFrame({'annee': df['date_pub'].unique()})
d_temps['id_temps'] = range(100, 100 + len(d_temps)) # Création d'une clé primaire
d_temps.to_csv("D_Temps.csv", index=False)

# 2. Dimension JOURNAL (D_Journal)
d_journal = pd.DataFrame({'nom_journal': df['journal'].unique()})
d_journal['id_journal'] = range(200, 200 + len(d_journal))
d_journal.to_csv("D_Journal.csv", index=False)

# 3. Dimension PAYS (D_Pays - pour la carte)
d_pays = pd.DataFrame({'nom_pays': df['country'].unique()})
d_pays['id_pays'] = range(300, 300 + len(d_pays))
d_pays.to_csv("D_Pays.csv", index=False)

# --- B. CRÉATION DE LA TABLE DE FAITS (F_Publications) --- [cite: 125]
# On remplace les textes par les ID des dimensions (Schéma en étoile)

df_fact = df.copy()
# Jointures pour récupérer les IDs
df_fact = df_fact.merge(d_temps, left_on='date_pub', right_on='annee')
df_fact = df_fact.merge(d_journal, left_on='journal', right_on='nom_journal')
df_fact = df_fact.merge(d_pays, left_on='country', right_on='nom_pays')

# Calcul des mesures
# Pour les auteurs, on compte le nombre de séparateurs ';' + 1
df_fact['nb_auteurs'] = df_fact['authors'].apply(lambda x: x.count(';') + 1)
df_fact['nb_publications'] = 1 # Chaque ligne est une publication

# Sélection des colonnes finales pour la table de faits
f_publications = df_fact[[
    'id_temps', 'id_journal', 'id_pays', 
    'nb_publications', 'nb_auteurs'
]]

f_publications.to_csv("F_Publications.csv", index=False)

print("Datawarehouse généré : F_Publications.csv, D_Temps.csv, D_Journal.csv, D_Pays.csv")
