# DataCo supply chain analytics

Analisi SQL su un dataset di supply chain globale (18.000+ ordini, 50+ variabili), con l'obiettivo di individuare pattern su tempi di consegna, ritardi e performance per categoria prodotto e regione.

## Dataset

[DataCo Smart Supply Chain for Big Data Analysis](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) — dati simulati su ordini, spedizioni, clienti e prodotti di un'azienda di distribuzione globale.

## Obiettivo

Rispondere a domande operative tipiche di un ruolo supply chain / ops:
- Quali regioni hanno i ritardi di consegna maggiori?
- Quali modalita' di spedizione sono piu' affidabili?
- Quali categorie prodotto generano piu' fatturato?
- Come varia il fatturato nel tempo?

## Setup

1. Scarica il CSV da Kaggle (link sopra) e posizionalo nella cartella del progetto
2. Crea il database: `CREATE DATABASE supply_chain;`
3. Installa le dipendenze: `pip install pandas mysql-connector-python sqlalchemy`
4. Aggiorna le credenziali MySQL in `dataco_starter.py`
5. Esegui `python dataco_starter.py` per caricare i dati ed eseguire le query di base

## Struttura

- `dataco_starter.py` — carica il CSV in MySQL ed esegue query KPI di esempio
- `queries/kpi_queries.sql` — tutte le query SQL scritte per l'analisi

## Risultati principali

*(da completare con i tuoi numeri effettivi, esempio sotto)*

- La regione con il ritardo medio di consegna piu' alto e' ... con ... giorni di ritardo medio
- La modalita' di spedizione piu' affidabile e' ..., con solo ...% di ordini a rischio ritardo
- La categoria "..." genera da sola il ...% del fatturato totale

## Prossimi passi

- Visualizzazione dei risultati in dashboard Power BI
- Modello di forecasting della domanda su dati mensili (progetto separato)

## Autore

Riccardo Rossi — [LinkedIn](https://linkedin.com/in/riccardorossi-471597250)
