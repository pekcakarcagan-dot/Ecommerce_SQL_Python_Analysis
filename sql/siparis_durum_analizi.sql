SELECT
    order_status,
    COUNT(*) as siparis_sayisi
FROM orders
GROUP BY order_status
ORDER BY siparis_sayisi DESC;