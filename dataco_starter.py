"""
Starter script - progetto 1: Inventory / Supply Chain Analytics
Dataset: DataCo Smart Supply Chain for Big Data Analysis
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

Cosa fa:
1. Carica il CSV scaricato da Kaggle in un database MySQL locale
2. Esegue alcune query KPI di esempio (lead time, ritardi, fatturato per categoria)
3. Stampa i risultati a schermo

Prima di eseguire:
- Installa MySQL Server e crea un database vuoto: CREATE DATABASE supply_chain;
- Scarica "DataCoSupplyChainDataset.csv" da Kaggle e mettilo in questa cartella
- pip install pandas mysql-connector-python sqlalchemy
- Aggiorna i parametri di connessione qui sotto (DB_USER, DB_PASSWORD)
"""

import re
import pandas as pd
from sqlalchemy import create_engine

CSV_PATH = "DataCoSupplyChainDataset.csv"
TABLE_NAME = "orders"

# --- Parametri di connessione MySQL: modifica con i tuoi valori ---
DB_USER = "root"
DB_PASSWORD = "Lunabred.01"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "supply_chain"

ENGINE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_engine():
    return create_engine(ENGINE_URL)


def load_csv_to_mysql():
    # Il file usa encoding latin-1, non utf-8
    df = pd.read_csv(CSV_PATH, encoding="latin-1")

    # Pulizia nomi colonna: minuscolo, spazi/parentesi/simboli -> underscore
    def clean_col(c):
        c = c.strip().lower()
        c = re.sub(r"[^a-z0-9]+", "_", c)   # tutto ciò che non e' lettera/numero -> _
        c = c.strip("_")
        return c

    df.columns = [clean_col(c) for c in df.columns]

    engine = get_engine()
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False, chunksize=5000)
    print(f"Caricate {len(df)} righe nel database '{DB_NAME}' (tabella '{TABLE_NAME}')")
    print("Colonne disponibili:")
    for col in df.columns:
        print(f"  - {col}")


def run_query(engine, title, query):
    print(f"\n--- {title} ---")
    result = pd.read_sql_query(query, engine)
    print(result.to_string(index=False))
    return result


def run_kpi_queries():
    engine = get_engine()

    # 1. Lead time medio: giorni di spedizione reali vs schedulati, per regione
    run_query(engine, "Lead time medio per regione", """
        SELECT order_region,
               ROUND(AVG(days_for_shipping_real), 2) AS giorni_reali_medi,
               ROUND(AVG(days_for_shipment_scheduled), 2) AS giorni_schedulati_medi,
               ROUND(AVG(days_for_shipping_real - days_for_shipment_scheduled), 2) AS ritardo_medio
        FROM orders
        GROUP BY order_region
        ORDER BY ritardo_medio DESC
        LIMIT 10;
    """)

    # 2. Tasso di consegna in ritardo per modalità di spedizione
    run_query(engine, "Percentuale ordini in ritardo per modalita' di spedizione", """
        SELECT shipping_mode,
               COUNT(*) AS totale_ordini,
               SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) AS ordini_a_rischio_ritardo,
               ROUND(100.0 * SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS perc_a_rischio
        FROM orders
        GROUP BY shipping_mode
        ORDER BY perc_a_rischio DESC;
    """)

    # 3. Top 10 categorie prodotto per fatturato
    run_query(engine, "Top 10 categorie prodotto per fatturato", """
        SELECT category_name,
               ROUND(SUM(sales), 2) AS fatturato_totale,
               COUNT(*) AS numero_ordini
        FROM orders
        GROUP BY category_name
        ORDER BY fatturato_totale DESC
        LIMIT 10;
    """)


if __name__ == "__main__":
    load_csv_to_mysql()
    run_kpi_queries()