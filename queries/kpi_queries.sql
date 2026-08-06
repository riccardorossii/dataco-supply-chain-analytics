SELECT DATE_FORMAT(STR_TO_DATE(order_date_dateorders, '%c/%e/%Y %H:%i'), '%Y-%m') AS mese,
       ROUND(SUM(sales), 2) AS fatturato_totale
FROM orders
GROUP BY DATE_FORMAT(STR_TO_DATE(order_date_dateorders, '%c/%e/%Y %H:%i'), '%Y-%m')
ORDER BY mese;

SELECT customer_id, COUNT(*) as numero_ordini
FROM orders
GROUP BY customer_id
ORDER BY numero_ordini desc LIMIT 10