# DataCo supply chain analytics

Analisi SQL su un dataset di supply chain globale (18.000+ ordini, 50+ variabili), con l'obiettivo di individuare pattern su tempi di consegna, ritardi e performance per categoria prodotto e regione.

## Dataset

[DataCo Smart Supply Chain for Big Data Analysis](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) — dati simulati su ordini, spedizioni, clienti e prodotti di un'azienda di distribuzione globale.

## Obiettivo

Rispondere a domande operative tipiche di una supply chain / ops:
- Quali regioni hanno i ritardi di consegna maggiori?
- Quali modalita' di spedizione sono piu' affidabili?
- Quali categorie prodotto generano piu' fatturato?
- Come varia il fatturato nel tempo?

## Struttura

- `dataco_starter.py` — carica il CSV in MySQL ed esegue query KPI di esempio
- `queries/kpi_queries.sql` — tutte le query SQL scritte per l'analisi

## Risultati principali

- La regione con il ritardo medio di consegna piu' alto è Central Asia con 0.65 giorni di ritardo medio
- La modalita' di spedizione piu' affidabile è Standard Class, con solo il 39% di ordini a rischio ritardo
- La categoria Fishing genera da sola circa 7 milioni di $ di fatturato, quasi il doppio della seconda categoria (Cleats)

## Visualizzazioni

![Ritardo medio per regione](images/ritardo_per_regione.png)

![Fatturato per categoria](images/fatturato_per_categoria.png)

![Andamento fatturato mensile](images/fatturato_mensile.png)

![Rischio ritardo per modalita' di spedizione](images/rischio_per_spedizione.png)

---

# Demand forecasting

Previsione del fatturato mensile a partire dai dati storici, confrontando un approccio semplice (media mobile) con un modello piu' avanzato (Prophet).

## Obiettivo

Rispondere a domande utili per la pianificazione operativa:
- Il fatturato ha un trend di crescita o di calo nel tempo?
- Esistono pattern stagionali ricorrenti?
- Quale fatturato aspettarsi nei prossimi mesi?

## Setup

1. Assicurati che il database MySQL `supply_chain` sia gia' popolato (vedi progetto 1)
2. Installa le dipendenze aggiuntive: `pip install jupyterlab prophet`
3. Avvia Jupyter Lab: `jupyter lab`
4. Apri `demand_forecasting.ipynb`, aggiorna le credenziali MySQL, esegui le celle in ordine

## Struttura

- `demand_forecasting.ipynb` - notebook con l'intera analisi: caricamento dati, media mobile, modello Prophet, verifica dei risultati

## Risultati principali

- Il fatturato mostra un **trend in calo** costante nel periodo osservato, passando da circa 1,08 milioni di dollari (fine 2014) a circa 0,89 milioni di dollari (inizio 2018)
- La stagionalita' annuale mostra un calo marcato a inizio gennaio e picchi ricorrenti tra fine ottobre e inizio novembre. Verificando il numero di ordini per mese, gennaio non presenta un volume di ordini inferiore agli altri mesi - il calo sembra quindi un pattern stagionale reale (es. rallentamento post-festivita'), non un artefatto di dati incompleti
- La previsione per i prossimi 3 mesi indica un fatturato stabile, attorno a 900.000 dollari al mese, con un intervallo di incertezza che si allarga progressivamente man mano che ci si allontana dai dati osservati
- Rispetto alla media mobile semplice, Prophet cattura meglio i pattern stagionali reali, che la media mobile tende a smussare o ignorare completamente

## Visualizzazioni

![Fatturato storico](images/fatturato_storico.png)

![Fatturato reale vs media mobile](images/media_mobile.png)

![Previsione Prophet](images/prophet_forecast.png)

![Componenti del modello (trend e stagionalita')](images/prophet_components.png)


---

# Report KPI automatico

Script Python che genera un report Excel con i KPI principali, direttamente dal database MySQL, senza doverli copiare a mano da Workbench ogni volta.

## Obiettivo

Automatizzare un task ripetitivo: invece di eseguire manualmente le 5 query KPI su Workbench e copiarle in Excel una per una, lo script fa tutto in un comando.

## Setup

1. Assicurati che il database MySQL `supply_chain` sia gia' popolato (vedi progetto 1)
2. Installa le dipendenze: `pip install pandas openpyxl sqlalchemy mysql-connector-python`
3. Aggiorna le credenziali MySQL nello script
4. Esegui: `python generate_kpi_report.py`

## Cosa fa

- Si connette al database MySQL
- Esegue le 5 query KPI (stesse del progetto 1)
- Scrive ogni risultato in un foglio Excel separato, con intestazioni in grassetto e colonne dimensionate automaticamente
- Salva il file con la data del giorno nel nome (es. `report_kpi_2026-08-06.xlsx`), cosi' ogni esecuzione produce un file nuovo senza sovrascrivere i precedenti

## Struttura

- `generate_kpi_report.py` - script principale

## Autore

Riccardo Rossi — [LinkedIn](https://linkedin.com/in/riccardorossi-471597250)
