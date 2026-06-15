import polars as pl
from prefect import task, context

@task
def cast_orders(df: pl.DataFrame) -> pl.DataFrame:

    logger = context.get("logger")

    logger.info(f"Start casting orders: {df.height} rows")

    df = df.with_columns([
        pl.col("order_id").cast(pl.Utf8),
        pl.col("customer_id").cast(pl.Utf8),
        pl.col("order_status").cast(pl.Utf8),

        pl.col("order_purchase_timestamp")
            .str.to_datetime(strict=False),

        pl.col("order_approved_at")
            .str.to_datetime(strict=False),

        pl.col("order_delivered_carrier_date")
            .str.to_datetime(strict=False),

        pl.col("order_delivered_customer_date")
            .str.to_datetime(strict=False),

        pl.col("order_estimated_delivery_date")
            .str.to_datetime(strict=False)
    ])

    logger.info("Finished casting orders")

    return df

@task
def cast_order_items(df: pl.DataFrame) -> pl.DataFrame:

    logger = context.get("logger")

    logger.info(f"Start casting order_items: {df.height} rows")

    df = df.with_columns([
        pl.col("order_id").cast(pl.Utf8),
        pl.col("order_item_id").cast(pl.Int64),

        pl.col("product_id").cast(pl.Utf8),
        pl.col("seller_id").cast(pl.Utf8),

        pl.col("shipping_limit_date")
            .str.to_datetime(strict=False),

        pl.col("price").cast(pl.Float64),
        pl.col("freight_value").cast(pl.Float64)
    ])

    logger.info("Finished casting order_items")

    return df

@task
def cast_payments(df: pl.DataFrame) -> pl.DataFrame:

    logger = context.get("logger")

    logger.info(f"Start casting payments: {df.height} rows")

    df = df.with_columns([
        pl.col("order_id").cast(pl.Utf8),

        pl.col("payment_sequential")
            .cast(pl.Int64),

        pl.col("payment_type")
            .cast(pl.Utf8),

        pl.col("payment_installments")
            .cast(pl.Int64),

        pl.col("payment_value")
            .cast(pl.Float64)
    ])

    logger.info("Finished casting payments")

    return df