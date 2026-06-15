CREATE OR REPLACE VIEW `living-os-project.mart.v_monthly_aov` AS

WITH order_level AS (
    SELECT
        order_id,
        DATE_TRUNC(DATE(order_purchase_timestamp), MONTH) AS order_month,
        MAX(total_payment_value) AS order_gmv
    FROM `living-os-project.intermediate.int_orders_enriched`
    GROUP BY 1,2
)

SELECT
    order_month,
    SUM(order_gmv) AS monthly_gmv,
    COUNT(order_id) AS total_orders,
    SAFE_DIVIDE(
        SUM(order_gmv),
        COUNT(order_id)
    ) AS average_order_value
FROM order_level
GROUP BY 1
ORDER BY 1;