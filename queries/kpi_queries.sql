SELECT DATE_FORMAT(STR_TO_DATE(order_date_dateorders, '%c/%e/%Y %H:%i'), '%Y-%m') AS mese,
       ROUND(SUM(sales), 2) AS fatturato_totale
FROM orders
GROUP BY DATE_FORMAT(STR_TO_DATE(order_date_dateorders, '%c/%e/%Y %H:%i'), '%Y-%m')
ORDER BY mese;