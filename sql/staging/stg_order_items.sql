CREATE TABLE IF NOT EXISTS `living-os-project.staging.stg_order_items` (
    order_id STRING,
    order_item_id INT64,
    product_id STRING,
    seller_id STRING,
    shipping_limit_date TIMESTAMP,
    price FLOAT64,
    freight_value FLOAT64
);