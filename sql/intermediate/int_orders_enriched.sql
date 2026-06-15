CREATE OR REPLACE TABLE `living-os-project.intermediate.int_orders_enriched` AS

WITH orders AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_delivered_customer_date,
        order_estimated_delivery_date,
        TIMESTAMP_DIFF(
            order_delivered_customer_date,
            order_purchase_timestamp,
            DAY
        ) AS delivery_lead_time_days
    FROM `living-os-project.staging.stg_orders`
),

items AS (
    SELECT 
        order_id,
        order_item_id,
        product_id,
        seller_id,
        price,
        freight_value
    FROM `living-os-project.staging.stg_order_items`
),

payments_aggregated AS (
    SELECT 
        order_id,
        SUM(payment_value) AS total_payment_value,
        ANY_VALUE(payment_type) AS primary_payment_type 
    FROM `living-os-project.staging.stg_payments`
    GROUP BY order_id
)

SELECT 
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    o.delivery_lead_time_days,
    i.order_item_id,
    i.product_id,
    i.seller_id,
    i.price,
    i.freight_value,
    p.total_payment_value,
    p.primary_payment_type
FROM orders o
LEFT JOIN items i 
    ON o.order_id = i.order_id
LEFT JOIN payments_aggregated p 
    ON o.order_id = p.order_id;