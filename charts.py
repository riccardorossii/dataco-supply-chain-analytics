"""
Genera grafici dalle query KPI del progetto DataCo Supply Chain Analytics.
Salva le immagini in una cartella 'images/' da caricare poi su GitHub.

Prima di eseguire:
- Assicurati che il database MySQL 'supply_chain' sia gia' popolato
  (esegui prima dataco_starter.py se non l'hai gia' fatto)
- pip install pandas sqlalchemy mysql-connector-python matplotlib
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# --- Parametri di connessione MySQL: stessi valori usati in dataco_starter.py ---
DB_USER = "root"
DB_PASSWORD = "Lunabred.01"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "supply_chain"

ENGINE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
OUTPUT_DIR = "images"

# Stile pulito per i grafici
plt.style.use("seaborn-v0_8-whitegrid")


def get_engine():
    return create_engine(ENGINE_URL)


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def chart_ritardo_per_regione(engine):
    query = """
        SELECT order_region,
               ROUND(AVG(days_for_shipping_real - days_for_shipment_scheduled), 2) AS ritardo_medio
        FROM orders
        GROUP BY order_region
        ORDER BY ritardo_medio DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, engine)

    plt.figure(figsize=(9, 5))
    plt.barh(df["order_region"], df["ritardo_medio"], color="#4C72B0")
    plt.xlabel("Ritardo medio (giorni)")
    plt.title("Ritardo medio di consegna per regione (top 10)")
    plt.gca().invert_yaxis()  # regione col ritardo maggiore in alto
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/ritardo_per_regione.png", dpi=150)
    plt.close()
    print("Salvato: ritardo_per_regione.png")


def chart_fatturato_per_categoria(engine):
    query = """
        SELECT category_name,
               ROUND(SUM(sales), 2) AS fatturato_totale
        FROM orders
        GROUP BY category_name
        ORDER BY fatturato_totale DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, engine)

    plt.figure(figsize=(9, 5))
    plt.barh(df["category_name"], df["fatturato_totale"], color="#55A868")
    plt.xlabel("Fatturato totale ($)")
    plt.title("Top 10 categorie prodotto per fatturato")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/fatturato_per_categoria.png", dpi=150)
    plt.close()
    print("Salvato: fatturato_per_categoria.png")


def chart_fatturato_mensile(engine):
    query = """
        SELECT DATE_FORMAT(STR_TO_DATE(order_date_dateorders, '%c/%e/%Y %H:%i'), '%Y-%m') AS mese,
               ROUND(SUM(sales), 2) AS fatturato_totale
        FROM orders
        GROUP BY DATE_FORMAT(STR_TO_DATE(order_date_dateorders, '%c/%e/%Y %H:%i'), '%Y-%m')
        ORDER BY mese;
    """
    df = pd.read_sql_query(query, engine)

    plt.figure(figsize=(10, 5))
    plt.plot(df["mese"], df["fatturato_totale"], marker="o", color="#C44E52")
    plt.xlabel("Mese")
    plt.ylabel("Fatturato totale ($)")
    plt.title("Andamento del fatturato mensile")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/fatturato_mensile.png", dpi=150)
    plt.close()
    print("Salvato: fatturato_mensile.png")


def chart_rischio_ritardo_per_spedizione(engine):
    query = """
        SELECT shipping_mode,
               ROUND(100.0 * SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS perc_a_rischio
        FROM orders
        GROUP BY shipping_mode
        ORDER BY perc_a_rischio DESC;
    """
    df = pd.read_sql_query(query, engine)

    plt.figure(figsize=(8, 5))
    plt.bar(df["shipping_mode"], df["perc_a_rischio"], color="#8172B2")
    plt.ylabel("% ordini a rischio ritardo")
    plt.title("Rischio ritardo per modalita' di spedizione")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/rischio_per_spedizione.png", dpi=150)
    plt.close()
    print("Salvato: rischio_per_spedizione.png")


if __name__ == "__main__":
    ensure_output_dir()
    engine = get_engine()
    chart_ritardo_per_regione(engine)
    chart_fatturato_per_categoria(engine)
    chart_fatturato_mensile(engine)
    chart_rischio_ritardo_per_spedizione(engine)
    print("\nTutti i grafici sono stati salvati nella cartella 'images/'.")