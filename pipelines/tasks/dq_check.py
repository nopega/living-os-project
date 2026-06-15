import polars as pl
from prefect import task, context


@task
def dq_orders(df: pl.DataFrame) -> pl.DataFrame:

    logger = context.get("logger")

    total_rows = df.height

    valid_df = df.filter(
        pl.col("order_id").is_not_null()
        & pl.col("customer_id").is_not_null()
    )

    rejected_rows = total_rows - valid_df.height

    if rejected_rows > 0:
        logger.warning(
            f"orders: rejected {rejected_rows} rows "
            f"(null order_id or customer_id)"
        )

    logger.info(
        f"[DQ_ORDERS] passed={valid_df.height} "
        f"rejected={rejected_rows}"
    )

    return valid_df

@task
def dq_order_items(df: pl.DataFrame) -> pl.DataFrame:

    logger = context.get("logger")

    total_rows = df.height

    valid_df = df.filter(
        pl.col("order_id").is_not_null()
        & (pl.col("price") > 0)
    )

    rejected_rows = total_rows - valid_df.height

    if rejected_rows > 0:
        logger.warning(
            f"order_items: rejected {rejected_rows} rows "
            f"(null keys or invalid price)"
        )

    logger.info(
        f"[DQ_ORDER_ITEMS] passed={valid_df.height} "
        f"rejected={rejected_rows}"
    )

    return valid_df

@task
def dq_payments(df: pl.DataFrame) -> pl.DataFrame:

    logger = context.get("logger")

    total_rows = df.height

    valid_df = df.filter(
        pl.col("order_id").is_not_null()
    )

    rejected_rows = total_rows - valid_df.height

    if rejected_rows > 0:
        logger.warning(
            f"payments: rejected {rejected_rows} rows"
        )

    logger.info(
        f"[DQ_PAYMENTS] passed={valid_df.height} "
        f"rejected={rejected_rows}"
    )

    return valid_df