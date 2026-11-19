-- 1. Total customers who placed delivered orders

SELECT
    COUNT(DISTINCT o.customer_id) AS total_customers
FROM orders o
WHERE o.order_status = 'delivered';


-- 2. Average order value

SELECT
    ROUND(
        SUM(oi.price)::numeric /
        COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';


-- 3. Top 10 customers by spending

SELECT
    o.customer_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price)::numeric, 2) AS total_spending

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY o.customer_id

ORDER BY total_spending DESC

LIMIT 10;