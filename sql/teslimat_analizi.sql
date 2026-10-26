
-- Teslimat Gecikme Analizi

-- 1. Geciken siparis sayisi
SELECT COUNT(*) AS geciken_siparis_sayisi
FROM orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date >
    order_estimated_delivery_date;

-- 2. Gecikme orani
SELECT
    ROUND(
        SUM(
            CASE
                WHEN order_delivered_customer_date >
                     order_estimated_delivery_date
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS gecikme_orani
FROM orders
WHERE order_status = 'delivered';

-- 3. Ortalama gecikme suresi
SELECT
    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_estimated_delivery_date
            )
        ), 2
    ) AS ortalama_gecikme_gunu
FROM orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date >
    order_estimated_delivery_date;


