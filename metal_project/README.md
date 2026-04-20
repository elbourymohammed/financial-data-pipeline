# metal_project

## Description

Projet dbt pour transformer les données financières brutes collectées dans PostgreSQL.
Le projet normalise les données brutes de métaux, crypto, devises et indicateurs macro-économiques, puis construit un mart d'analyse globale.

## Structure du projet

- `dbt_project.yml` : configuration dbt du projet.
- `models/staging/` : modèles de staging qui nettoient et standardisent les sources brutes.
- `models/marts/` : modèles analytiques finaux.
- `models/staging/schema.yml` : définitions de sources et tests de qualité.

## Sources attendues

Les tables brutes doivent exister dans le schéma `public` de PostgreSQL :

- `raw_metal_prices`
- `raw_crypto_prices`
- `raw_fx_rates`
- `raw_macro_indicators`

## Modèles principaux

### `models/staging/stg_metal_prices.sql`

- Lit `raw_metal_prices` depuis la source `public.raw_metal_prices`.
- Convertit les colonnes en majuscules.
- Arrondit les valeurs numériques.
- Calcule `change` et `change_percent` par métal.
- Filtre les doublons et les enregistrements sans prix.
- Tests définis :
  - `accepted_values` pour `metal` (`GOLD`, `SILVER`, `PLATINIUM`)
  - `not_null` pour `price`

### `models/staging/stg_crypto_prices.sql`

- Nettoie les données crypto.
- Fournit un prix par date et par crypto.
- Tests définis :
  - `not_null` pour `price`

### `models/staging/stg_fx_rates.sql`

- Prépare les taux de change.
- Tests définis :
  - `not_null` pour `date`
  - `not_null` pour `rate`

### `models/staging/stg_macro_indicators.sql`

- Normalise les indicateurs macro-économiques.
- Tests définis :
  - `not_null` pour `date`
  - `not_null` pour `indicator_name`
  - `not_null` pour `value`

### `models/marts/mart_financial_overview.sql`

- Agrège les données de métaux avec les prix crypto, les taux de change et les indicateurs macro.
- Effectue des pivots pour :
  - prix Bitcoin
  - taux USD/EUR, USD/GBP, USD/JPY, USD/CHF
  - indicateurs `UNEMPLOYMENT`, `INFLATION`, `TOTAL PRODUCTION VALUE`
- Produit un jeu de résultats unifié par métal et par date.

## Matérialisation

Dans `dbt_project.yml`, les modèles de `staging` et `marts` sont configurés avec `+materialized: table`.

## Commandes utiles

```bash
cd metal_project
dbt debug
dbt run --full-refresh
dbt test
dbt compile
```

## Notes importantes

- Ce projet dbt repose sur un profil dbt nommé `metal_project`.
- La source `public` est hardcodée dans `models/staging/schema.yml`.
- `mart_financial_overview` s'appuie sur des correspondances de dates entre métaux, crypto, FX et macro, et utilise les valeurs historiques les plus récentes des indicateurs macro.

## Astuces

- Vérifiez d'abord que les tables `raw_*` sont remplies.
- Lancez `dbt test` après `dbt run` pour valider la qualité des données.
- Si vous changez de schéma ou de profil, mettez à jour `dbt_project.yml` et `models/staging/schema.yml`.
