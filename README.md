# 🚀 Scientific Research Analysis Platform (Big Data & BI)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Spark](https://img.shields.io/badge/Apache%20Spark-3.x-orange)
![Hadoop](https://img.shields.io/badge/Hadoop-HDFS-yellow)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green)
![Flask](https://img.shields.io/badge/Backend-Flask-red)

## 📋 Présentation du Projet

Ce projet est une solution complète de **Business Intelligence (BI) et Big Data** dédiée à l'analyse de la production scientifique mondiale (Cas d'étude : **Blockchain**).

Il implémente un pipeline de données complet ("End-to-End") couvrant les 4 phases du cycle de vie de la donnée :
1.  **Collecte (Scraping)** : Extraction automatisée de métadonnées depuis IEEE, ScienceDirect et ACM.
2.  **Stockage (Data Lake)** : Architecture hybride NoSQL (MongoDB) et Distribuée (Hadoop HDFS).
3.  **Traitement (ETL & NLP)** : Nettoyage, modélisation en étoile (Data Warehouse) et analyse sémantique (LDA) avec **Apache Spark**.
4.  **Visualisation (Dashboard)** : Interface Web interactive avec Cartographie et Text Mining.

---

## 🏗️ Architecture Technique

Le projet suit une architecture en couches :

| Phase | Technologie | Rôle |
| :--- | :--- | :--- |
| **Ingestion** | **Scrapy** (Python) | Robots d'indexation (Spiders) pour collecter les articles. |
| **Stockage** | **HDFS** & **MongoDB** | Stockage des données brutes (JSON) et indexation temps réel. |
| **Processing** | **PySpark** (Spark SQL/MLlib) | ETL, Création des Dimensions/Faits, NLP (TF-IDF, LDA). |
| **Backend** | **Flask** (Python) | API REST exposant les données du Data Warehouse. |
| **Frontend** | **Chart.js**, **Highcharts** | Tableaux de bord, Cartes interactives, Nuages de mots. |

---

## 📂 Structure du Projet

```text
/Project_Root
│
├── /Data_Collection          # PHASE 1 : SCRAPING
│   ├── run_all.py            # Script d'orchestration
│   ├── /ACM                  # Spider ACM
│   ├── /IEE                  # Spider IEEE
│   └── /SCIENCE_DIRECT       # Spider ScienceDirect
│
├── /Data_Processing          # PHASE 3 : SPARK
│   ├── analysis_notebook.ipynb # Notebook Jupyter (ETL + NLP)
│   └── keywords.csv          # Output: Mots-clés générés
│
├── /Dashboard                # PHASE 4 : WEB APP
│   ├── app.py                # Serveur Flask (API)
│   ├── F_Publications.csv    # Table de Faits (Générée par Spark)
│   ├── D_Temps.csv           # Dimension Temps
│   ├── D_Pays.csv            # Dimension Pays
│   ├── D_Journal.csv         # Dimension Journal
│   └── /templates
│       └── index.html        # Interface Frontend
│
└── README.md                 # Documentation
