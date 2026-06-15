CREATE OR REPLACE VIEW `living-os-project.mart.v_monthly_on_time_delivery_rate` AS

SELECT
    DATE_TRUNC(DATE(order_purchase_timestamp), MONTH) AS order_month,

    COUNT(*) AS delivered_orders,

    COUNTIF(
        order_delivered_customer_date
        <= order_estimated_delivery_date
    ) AS on_time_orders,

    SAFE_DIVIDE(
        COUNTIF(
            order_delivered_customer_date
            <= order_estimated_delivery_date
        ),
        COUNT(*)
    ) * 100 AS on_time_delivery_rate_pct

FROM `living-os-project.staging.stg_orders`
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY 1;