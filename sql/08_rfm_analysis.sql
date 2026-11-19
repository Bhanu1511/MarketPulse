WITH customer_metrics AS (

    SELECT
        c.customer_unique_id,

        MAX(o.order_purchase_timestamp::timestamp)
            AS last_purchase_date,

        COUNT(DISTINCT o.order_id)
            AS frequency,

        SUM(oi.price)
            AS monetary

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'delivered'

    GROUP BY c.customer_unique_id
),

rfm AS (

    SELECT
        customer_unique_id,

        (
            DATE '2018-10-01'
            - last_purchase_date::date
        ) AS recency,

        frequency,

        monetary

    FROM customer_metrics
)

SELECT
    customer_unique_id,
    recency,
    frequency,

    ROUND(monetary::numeric, 2) AS monetary,

    NTILE(5) OVER (
        ORDER BY recency DESC
    ) AS recency_score,

    NTILE(5) OVER (
        ORDER BY frequency
    ) AS frequency_score,

    NTILE(5) OVER (
        ORDER BY monetary
    ) AS monetary_score

FROM rfm

ORDER BY monetary DESC

LIMIT 20;