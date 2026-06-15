CREATE TABLE IF NOT EXISTS `living-os-project.staging.stg_payments` (
    order_id STRING,
    payment_sequential INT64,
    payment_type STRING,
    payment_installments INT64,
    payment_value FLOAT64
);