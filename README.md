# Data Project

## Description

Pipeline de données financières et métaux précieux.
Le projet collecte des données brutes depuis plusieurs sources, les stocke dans une base PostgreSQL, puis les transforme avec dbt pour produire des modèles analytiques.

## Objectif

- Rendre l'ingestion testable et réutilisable.
- Séparer la logique métier (services) de l'exécution (runners / Airflow).
- Orchestrer la collecte et la transformation avec Airflow et dbt.

## Architecture

- `src/`
  - `database/Database.py` : connexion PostgreSQL et wrapper d'exécution SQL.
  - `runners/` : orchestration des ingestions par domaine (crypto, FX, macro, métaux).
  - `services/` : logique métier d'appel API et génération de dates.
  - `repositories/` : insertion des données dans les tables `raw_*`.
- `airflow/dags/financial_pipeline_dag.py` : DAG Airflow principal.
- `metal_project/` : projet dbt de transformation.
  - `models/staging/` : staging des données brutes.
  - `models/marts/` : modèles analytiques.

## Fonctionnalités

- Ingestion des métaux précieux via l'API GoldAPI.
- Ingestion de cryptomonnaies, taux de change et indicateurs macroéconomiques.
- Transformation dbt avec tests de qualité.
- Orchestration Airflow pour exécuter ingestion, dbt run et dbt test.

## Limites actuelles

- **Quotas API** : l'analyse est restreinte par les limitations de nombre de requêtes des APIs utilisées. Chaque source (GoldAPI, CoinGecko, FX, FRED) a ses propres contraintes de rate-limiting.
Ne possibilité d'historique complet** : pour étendre l'horizon d'analyse, il faudrait gérer les quotas, implémenter un cache, et configurer une orchestration complète avec retry logic.

## Prérequis

- Python 3.11+ (ou version compatible avec les dépendances)
- PostgreSQL
- Airflow installé et configuré si vous souhaitez exécuter le DAG.
- dbt installé pour la transformation.

## Installation

```bash
cd /path/to/Data_Project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Configuration

Créer un fichier `.env` à la racine du projet avec au moins :

```env
# PostgreSQL Database
#DATABASE_URL=DATABASE_URL
#DB_HOST=DB_HOST
#DB_PORT=DB_PORT
#DB_NAME=DB_NAME
#DB_USER=DB_USER
#DB_PASSWORD=DB_PASSWORD

# API Keys
#METAL_API_KEY=YOUR_METAL_API_KEY
#FX_API_TOKEN=YOUR_FX_API_TOKEN
#FRED_API_KEY=YOUR_FRED_API_KEY

# Logging Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
```

## Exécution

Le pipeline est orchestré automatiquement via Airflow.

### Airflow (Production)

Le DAG `financial_pipeline` s'exécute automatiquement **chaque jour à minuit** (0 0 * * *).

Chaque exécution :
1. Récupère les données de la veille via les runners (en parallèle) :
   - `ingest_crypto` - prix Bitcoin
   - `ingest_fx_rates` - taux de change
   - `ingest_macro_indicators` - indicateurs macro
   - `ingest_metal` - prix des métaux
2. Lance la transformation dbt : `dbt run --full-refresh`
3. Exécute les tests dbt : `dbt test`

Le DAG est défini dans [airflow/dags/financial_pipeline_dag.py](airflow/dags/financial_pipeline_dag.py).

### Exécution manuelle (Développement)

Pour exécuter manuellement les runners :

```bash
python src/runners/crypto_runner.py
python src/runners/fx_rates_runner.py
python src/runners/macro_indicators_runner.py
python src/runners/metal_runner.py
```

Chaque runner récupère automatiquement les données du jour précédent.

## dbt

Le projet dbt se trouve dans `metal_project/`.

Commandes utiles :

```bash
cd metal_project
dbt run --full-refresh
dbt test
```

Le fichier `metal_project/dbt_project.yml` précise que les modèles `staging` et `marts` sont matérialisés en tables.

## Tests

Le projet contient des tests simples dans `tests/`.
L'environnement de test utilise `pytest` :

```bash
pytest tests
```

## Structure du dépôt

- `airflow/dags/`
- `metal_project/`
- `src/`
- `tests/`
- `requirements.txt`
- `setup.py`
