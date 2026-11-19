WITH monthly_revenue AS (

    SELECT
        DATE_TRUNC(
            'month',
            o.order_purchase_timestamp::timestamp
        ) AS month,

        SUM(oi.price) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'delivered'

    GROUP BY 1
),

revenue_comparison AS (

    SELECT
        month,
        revenue,

        LAG(revenue) OVER (
            ORDER BY month
        ) AS previous_month_revenue

    FROM monthly_revenue
)

SELECT
    month,

    ROUND(revenue::numeric, 2) AS current_revenue,

    ROUND(previous_month_revenue::numeric, 2)
        AS previous_revenue,

    ROUND(
        (
            (revenue - previous_month_revenue)
            / NULLIF(previous_month_revenue, 0)
        * 100)::numeric,
        2
    ) AS growth_percentage

FROM revenue_comparison

ORDER BY month;