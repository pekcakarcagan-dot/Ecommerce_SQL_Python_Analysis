
SELECT
    c.customer_city AS sehir,
    COUNT(*) AS toplam_teslimat,

    SUM(
        CASE
            WHEN o.order_delivered_customer_date >
                 o.order_estimated_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS geciken_siparis,

    ROUND(
        SUM(
            CASE
                WHEN o.order_delivered_customer_date >
                     o.order_estimated_delivery_date
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS gecikme_orani

FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY c.customer_city

HAVING COUNT(*) >= 100

ORDER BY gecikme_orani DESC
LIMIT 10;
 


-- Sao Paulo ve Maceio gecikme karsilastirmasi

SELECT
    c.customer_city AS sehir,
    COUNT(*) AS toplam_teslimat,
    SUM(
        CASE
            WHEN o.order_delivered_customer_date >
                 o.order_estimated_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS geciken_siparis,
    ROUND(
        SUM(
            CASE
                WHEN o.order_delivered_customer_date >
                     o.order_estimated_delivery_date
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS gecikme_orani
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
  AND c.customer_city IN ('sao paulo', 'maceio')
GROUP BY c.customer_city
ORDER BY geciken_siparis DESC;
