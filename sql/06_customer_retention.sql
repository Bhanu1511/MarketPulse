WITH customer_orders AS (

    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders

    FROM orders

    WHERE order_status = 'delivered'

    GROUP BY customer_id
)

SELECT
    CASE
        WHEN total_orders = 1 THEN 'One-time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,

    COUNT(*) AS total_customers

FROM customer_orders

GROUP BY customer_type

ORDER BY total_customers DESC;