import os
import polars as pl

from prefect import task, context
from google.cloud import bigquery
from google.oauth2 import service_account

PARQUET_DIR = "./parquet_folder"


# =========================
# BigQuery Schemas
# =========================
BQ_SCHEMAS = {
    "stg_order_items": [
        bigquery.SchemaField("order_id", "STRING"),
        bigquery.SchemaField("order_item_id", "INT64"),
        bigquery.SchemaField("product_id", "STRING"),
        bigquery.SchemaField("seller_id", "STRING"),
        bigquery.SchemaField("shipping_limit_date", "TIMESTAMP"),
        bigquery.SchemaField("price", "FLOAT"),
        bigquery.SchemaField("freight_value", "FLOAT"),
    ],
    "stg_orders": [
        bigquery.SchemaField("order_id", "STRING"),
        bigquery.SchemaField("customer_id", "STRING"),
        bigquery.SchemaField("order_status", "STRING"),
        bigquery.SchemaField("order_purchase_timestamp", "TIMESTAMP"),
        bigquery.SchemaField("order_approved_at", "TIMESTAMP"),
        bigquery.SchemaField("order_delivered_carrier_date", "TIMESTAMP"),
        bigquery.SchemaField("order_delivered_customer_date", "TIMESTAMP"),
        bigquery.SchemaField("order_estimated_delivery_date", "TIMESTAMP"),
    ],
    "stg_payments": [
        bigquery.SchemaField("order_id", "STRING"),
        bigquery.SchemaField("payment_sequential", "INT64"),
        bigquery.SchemaField("payment_type", "STRING"),
        bigquery.SchemaField("payment_installments", "INT64"),
        bigquery.SchemaField("payment_value", "FLOAT"),
    ],
}


def get_bq_client(project_id: str):
    key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not key_path:
        raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS")

    credentials = service_account.Credentials.from_service_account_file(
        key_path
    )

    return bigquery.Client(
        project=project_id,
        credentials=credentials
    )


@task
def load_to_bigquery(
    df: pl.DataFrame,
    project_id: str,
    dataset_id: str,
    table_id: str,
    write_disposition: str = "WRITE_TRUNCATE",
):

    logger = context.get("logger")

    os.makedirs(PARQUET_DIR, exist_ok=True)

    client = get_bq_client(project_id)

    target_table = f"{project_id}.{dataset_id}.{table_id}"

    schema = BQ_SCHEMAS.get(table_id)

    if not schema:
        raise ValueError(f"Schema not found for table: {table_id}")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=write_disposition,
        schema=schema,
        create_disposition="CREATE_IF_NEEDED",
    )

    batch_size = 20000  # 👈 ปรับได้
    total_rows = df.height

    logger.info(
        f"Start batch loading: {total_rows} rows, batch_size={batch_size}"
    )

    try:
        for i in range(0, total_rows, batch_size):

            batch_df = df.slice(i, batch_size)

            batch_path = os.path.join(
                PARQUET_DIR,
                f"{table_id}_part_{i}.parquet"
            )

            logger.info(f"[BATCH] Saving {batch_path}")

            batch_df.write_parquet(batch_path)

            with open(batch_path, "rb") as f:
                job = client.load_table_from_file(
                    f,
                    target_table,
                    job_config=job_config,
                )

            job.result()

            logger.info(
                f"[BATCH] Loaded {batch_df.height} rows "
                f"({i} → {i + batch_df.height})"
            )

        logger.info(f"[DONE] {total_rows} rows loaded to {target_table}")

    except Exception as e:
        logger.error(f"BigQuery load failed: {str(e)}")
        raise