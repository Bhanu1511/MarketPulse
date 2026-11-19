SELECT
    DATE_TRUNC(
        'month',
        o.order_purchase_timestamp::timestamp
    ) AS month,

    ROUND(SUM(oi.price)::numeric, 2) AS total_revenue,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(AVG(oi.price)::numeric, 2) AS average_item_price

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY 1

ORDER BY 1;