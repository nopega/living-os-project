import os
import polars as pl

from prefect import task, context


DATA_DIR = "./data"


@task
def extract_csv(filename: str) -> pl.DataFrame:

    logger = context.get("logger")

    file_path = os.path.join(
        DATA_DIR,
        filename
    )

    logger.info(
        f"Start extracting file: {file_path}"
    )

    if not os.path.exists(file_path):
        logger.error(
            f"File not found: {file_path}"
        )
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    df = pl.read_csv(file_path)

    logger.info(
        f"[EXTRACT] {filename} -> "
        f"{df.height} rows, {df.width} columns"
    )

    return df