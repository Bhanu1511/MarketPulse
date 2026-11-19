-- Delivery performance overview

SELECT

    CASE
        WHEN order_delivered_customer_date::timestamp
             <= order_estimated_delivery_date::timestamp
        THEN 'On Time'

        ELSE 'Late'
    END AS delivery_status,

    COUNT(*) AS total_orders,

    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date::timestamp
                    - order_purchase_timestamp::timestamp
                )
            ) / 86400
        )::numeric,
        2
    ) AS average_delivery_days

FROM orders

WHERE order_status = 'delivered'

AND order_delivered_customer_date IS NOT NULL

AND order_estimated_delivery_date IS NOT NULL

GROUP BY 1

ORDER BY total_orders DESC;