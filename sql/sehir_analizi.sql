
SELECT
    c.customer_city,
    COUNT(o.order_id) AS toplam_siparis
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_city
ORDER BY toplam_siparis DESC
LIMIT 10;
