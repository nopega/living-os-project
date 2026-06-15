CREATE OR REPLACE VIEW `living-os-project.mart.mart_daily_revenue` AS

SELECT
    DATE(order_purchase_timestamp) AS order_date,

    SUM(price) AS gmv,

    COUNT(DISTINCT order_id) AS total_orders

FROM `living-os-project.intermediate.int_orders_enriched`

GROUP BY 1
ORDER BY 1;