-- Top 10 products by revenue

SELECT
    p.product_id,

    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    SUM(oi.order_item_id) AS total_items_sold,

    ROUND(SUM(oi.price)::numeric, 2) AS total_revenue

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

JOIN orders o
    ON oi.order_id = o.order_id

LEFT JOIN category_translation t
    ON p.product_category_name = t.product_category_name

WHERE o.order_status = 'delivered'

GROUP BY
    p.product_id,
    category

ORDER BY total_revenue DESC

LIMIT 10;