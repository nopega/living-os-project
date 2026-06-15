import os
from dotenv import load_dotenv

from prefect import Flow

from tasks.download import download_dataset
from tasks.extract import extract_csv

from tasks.cast import (
    cast_orders,
    cast_order_items,
    cast_payments,
)

from tasks.dq_check import (
    dq_orders,
    dq_order_items,
    dq_payments,
)

from tasks.load import load_to_bigquery


# =========================
# LOAD ENV
# =========================
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")


with Flow("olist-etl-pipeline") as flow:

    # =========================
    # 1. DOWNLOAD STEP
    # =========================
    download_path = download_dataset()

    # =========================
    # 2. ORDERS PIPELINE
    # =========================
    orders_raw = extract_csv(
        "olist_orders_dataset.csv",
        upstream_tasks=[download_path]
    )

    orders_cast = cast_orders(orders_raw)
    orders_dq = dq_orders(orders_cast)

    load_orders = load_to_bigquery(
        orders_cast,
        PROJECT_ID,
        DATASET_ID,
        "stg_orders",
    )
    load_orders.set_upstream(orders_dq)

    # =========================
    # 3. ORDER ITEMS PIPELINE
    # =========================
    items_raw = extract_csv(
        "olist_order_items_dataset.csv",
        upstream_tasks=[download_path]
    )

    items_cast = cast_order_items(items_raw)
    items_dq = dq_order_items(items_cast)

    load_items = load_to_bigquery(
        items_cast,
        PROJECT_ID,
        DATASET_ID,
        "stg_order_items",
    )
    load_items.set_upstream(items_dq)

    # =========================
    # 4. PAYMENTS PIPELINE
    # =========================
    payments_raw = extract_csv(
        "olist_order_payments_dataset.csv",
        upstream_tasks=[download_path]
    )

    payments_cast = cast_payments(payments_raw)
    payments_dq = dq_payments(payments_cast)

    load_payments = load_to_bigquery(
        payments_cast,
        PROJECT_ID,
        DATASET_ID,
        "stg_payments",
    )
    load_payments.set_upstream(payments_dq)


if __name__ == "__main__":
    flow.run()