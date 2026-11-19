-- 1. Distribution of review scores

SELECT
    review_score,
    COUNT(*) AS total_reviews,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage

FROM reviews

GROUP BY review_score

ORDER BY review_score;


-- 2. Average review score

SELECT
    ROUND(AVG(review_score)::numeric, 2)
        AS average_review_score

FROM reviews;


-- 3. Review score by delivery status

SELECT
    CASE
        WHEN o.order_delivered_customer_date::timestamp
             <= o.order_estimated_delivery_date::timestamp
        THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status,

    COUNT(r.review_id) AS total_reviews,

    ROUND(AVG(r.review_score)::numeric, 2)
        AS average_review_score

FROM orders o

JOIN reviews r
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'

AND o.order_delivered_customer_date IS NOT NULL

AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY 1

ORDER BY 1;