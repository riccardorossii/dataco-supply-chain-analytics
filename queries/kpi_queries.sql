-- ============================================================
-- DataCo Supply Chain Analytics - Query KPI
-- Database: supply_chain | Tabella: orders
-- ============================================================

USE supply_chain;

-- 1. Lead time medio: giorni di spedizione reali vs schedulati, per regione
SELECT order_region,
       ROUND(AVG(days_for_shipping_real), 2) AS giorni_reali_medi,
       ROUND(AVG(days_for_shipment_scheduled), 2) AS giorni_schedulati_medi,
       ROUND(AVG(days_for_shipping_real - days_for_shipment_scheduled), 2) AS ritardo_medio
FROM orders
GROUP BY order_region
ORDER BY ritardo_medio DESC
LIMIT 10;

-- 2. Percentuale ordini a rischio ritardo, per modalita' di spedizione
SELECT shipping_mode,
       COUNT(*) AS totale_ordini,
       SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) AS ordini_a_rischio_ritardo,
       ROUND(100.0 * SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS perc_a_rischio
FROM orders
GROUP BY shipping_mode
ORDER BY perc_a_rischio DESC;

-- 3. Top 10 categorie prodotto per fatturato
SELECT category_name,
       ROUND(SUM(sales), 2) AS fatturato_totale,
       COUNT(*) AS numero_ordini
FROM orders
GROUP BY category_name
ORDER BY fatturato_totale DESC
LIMIT 10;

-- 4. Fatturato mensile nel tempo
-- La colonna data e' salvata come testo (formato M/D/YYYY H:MM), va convertita prima
SELECT DATE_FORMAT(STR_TO_DATE(order_date_dateorders, '%c/%e/%Y %H:%i'), '%Y-%m') AS mese,
       ROUND(SUM(sales), 2) AS fatturato_totale
FROM orders
GROUP BY DATE_FORMAT(STR_TO_DATE(order_date_dateorders, '%c/%e/%Y %H:%i'), '%Y-%m')
ORDER BY mese;

-- 5. Top 10 clienti per numero di ordini
SELECT customer_id, COUNT(*) AS numero_ordini
FROM orders
GROUP BY customer_id
ORDER BY numero_ordini DESC
LIMIT 10;