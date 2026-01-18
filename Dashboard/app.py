from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
import os
import re

app = Flask(__name__)
CORS(app)

# --- Configuration MongoDB ---
client = MongoClient('mongodb://localhost:27017/')
db = client['aci']
collection = db['articles']

# --- Configuration des Fichiers Data Warehouse (Phase 4) ---
DWH_FILES = {
    'fact': 'F_Publications.csv',
    'dim_time': 'D_Temps.csv',
    'dim_journal': 'D_Journal.csv',
    'dim_country': 'D_Pays.csv',
    'top_authors': 'top_authors.csv',
    'keywords': 'keywords.csv'  # <--- AJOUT POUR PHASE 4 (Word Cloud)
}

# --- Fonction Helper : Reconstruire le modèle en étoile ---
def load_datawarehouse():
    try:
        if not os.path.exists(DWH_FILES['fact']): return None
        df_fact = pd.read_csv(DWH_FILES['fact'])

        if os.path.exists(DWH_FILES['dim_time']):
            df_time = pd.read_csv(DWH_FILES['dim_time'])
            df_fact = df_fact.merge(df_time, on='id_temps', how='left')

        if os.path.exists(DWH_FILES['dim_journal']):
            df_journal = pd.read_csv(DWH_FILES['dim_journal'])
            df_fact = df_fact.merge(df_journal, on='id_journal', how='left')

        if os.path.exists(DWH_FILES['dim_country']):
            df_country = pd.read_csv(DWH_FILES['dim_country'])
            df_fact = df_fact.merge(df_country, on='id_pays', how='left')
            
        return df_fact
    except Exception as e:
        print(f"Erreur DWH : {e}")
        return None

# --- Routes ---

@app.route('/')
def dashboard():
    return render_template('index.html')

# 1. OVERVIEW (KPIs)
@app.route('/api/stats/overview', methods=['GET'])
def get_overview():
    try:
        total = collection.count_documents({})
        stats = {
            "total_articles": total,
            "total_sources": len(collection.distinct("source")),
            "total_journals": len(collection.distinct("journal")),
            "year_range": {"min": 2019, "max": 2025}
        }
        return jsonify({"statistics": stats})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. EVOLUTION ANNUELLE (Trend Analysis - Phase 3 & 4)
@app.route('/api/stats/by-year', methods=['GET'])
def get_by_year():
    df = load_datawarehouse()
    if df is not None:
        trend = df.groupby('annee')['nb_publications'].sum().reset_index()
        trend = trend.sort_values('annee')
        data = trend.rename(columns={'annee': 'year', 'nb_publications': 'count'}).to_dict(orient='records')
        return jsonify({"data": data})
    else:
        return jsonify({"data": []})

# 3. TOP JOURNAUX (Couvre "Top Laboratoires/Journaux" - Phase 4)
@app.route('/api/stats/by-journal', methods=['GET'])
def get_by_journal():
    df = load_datawarehouse()
    if df is not None:
        top = df.groupby('nom_journal')['nb_publications'].sum().reset_index()
        top = top.sort_values('nb_publications', ascending=False).head(10)
        data = top.rename(columns={'nom_journal': 'journal', 'nb_publications': 'count'}).to_dict(orient='records')
        return jsonify({"data": data})
    else:
        return jsonify({"data": []})

# 4. CARTE MONDIALE (Production par pays - Phase 4)
@app.route('/api/stats/by-country', methods=['GET'])
def get_by_country():
    df = load_datawarehouse()
    if df is not None:
        by_country = df.groupby('nom_pays')['nb_publications'].sum().reset_index()
        data = by_country.rename(columns={'nom_pays': 'country', 'nb_publications': 'count'}).to_dict(orient='records')
        return jsonify({"data": data})
    else:
        return jsonify({"data": []})

# 5. QUARTILES (Qualité Scientifique - Phase 3 & 4)
@app.route('/api/stats/quartiles', methods=['GET'])
def get_quartiles():
    df = load_datawarehouse()
    if df is not None:
        q = df.groupby('quartile')['nb_publications'].sum().reset_index()
        data = q.rename(columns={'nb_publications': 'count'}).to_dict(orient='records')
        return jsonify({"data": data})
    else:
        return jsonify({"data": []})

# 6. TOP AUTEURS (Productivité - Phase 3 & 4)
@app.route('/api/stats/top-authors', methods=['GET'])
def get_top_authors():
    if os.path.exists(DWH_FILES['top_authors']):
        try:
            df = pd.read_csv(DWH_FILES['top_authors'])
            # Renommage sécurisé selon ce que Spark a généré
            if 'author_name' in df.columns:
                df = df.rename(columns={'author_name': 'author'})
            data = df.head(15)[['author', 'count']].to_dict(orient='records')
            return jsonify({"data": data})
        except:
             return jsonify({"data": []})
    return jsonify({"data": []})

# 7. MOTS-CLÉS / THÉMATIQUES (Pour le Word Cloud - Phase 4 Onglet 4) <--- NOUVEAU
@app.route('/api/stats/keywords', methods=['GET'])
def get_keywords():
    """
    Charge les mots-clés ou topics générés par Spark (LDA/TF-IDF)
    """
    if os.path.exists(DWH_FILES['keywords']):
        try:
            df = pd.read_csv(DWH_FILES['keywords'])
            # On s'attend à des colonnes : 'word', 'weight'
            data = df.head(50).to_dict(orient='records')
            return jsonify({"data": data})
        except Exception as e:
            print(f"Erreur Keywords: {e}")
            return jsonify({"data": []})
    else:
        # Données de secours si Spark n'a pas encore généré le CSV
        fallback = [
            {"name": "Machine Learning", "weight": 30},
            {"name": "Big Data", "weight": 25},
            {"name": "Blockchain", "weight": 20},
            {"name": "IoT", "weight": 15},
            {"name": "Security", "weight": 10}
        ]
        return jsonify({"data": fallback})

# 8. RECHERCHE (Mongo)
@app.route('/api/search', methods=['GET'])
def search_articles():
    query_str = request.args.get('query', '')
    if not query_str: return jsonify([])
    regex = re.compile(query_str, re.IGNORECASE)
    results = list(collection.find({"$or": [{"title": regex}, {"authors": regex}]}, {"_id": 0}).limit(20))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)