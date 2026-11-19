WITH customer_metrics AS (

    SELECT
        c.customer_unique_id,

        MAX(o.order_purchase_timestamp::timestamp) AS last_purchase,

        COUNT(DISTINCT o.order_id) AS frequency,

        SUM(oi.price) AS monetary

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

        DATE '2018-10-01' - last_purchase::date AS recency,

        frequency,

        monetary,

        NTILE(5) OVER (
            ORDER BY DATE '2018-10-01' - last_purchase::date DESC
        ) AS r_score,

        NTILE(5) OVER (
            ORDER BY frequency
        ) AS f_score,

        NTILE(5) OVER (
            ORDER BY monetary
        ) AS m_score

    FROM customer_metrics
),

segments AS (

    SELECT
        *,

        CASE
            WHEN r_score >= 4 AND f_score >= 4
                THEN 'Champions'

            WHEN r_score >= 3 AND f_score >= 4
                THEN 'Loyal Customers'

            WHEN r_score >= 4 AND f_score <= 2
                THEN 'New Customers'

            WHEN r_score <= 2 AND f_score >= 3
                THEN 'At Risk'

            WHEN r_score <= 2 AND f_score <= 2
                THEN 'Hibernating'

            ELSE 'Potential Loyalists'
        END AS customer_segment

    FROM rfm
)

SELECT
    customer_segment,

    COUNT(*) AS total_customers,

    ROUND(AVG(monetary)::numeric, 2) AS average_spending

FROM segments

GROUP BY customer_segment

ORDER BY total_customers DESC;