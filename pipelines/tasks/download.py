import os
import shutil
import kagglehub

from prefect import task, context


@task
def download_dataset():

    logger = context.get("logger")

    logger.info(
        "Starting Kaggle dataset download..."
    )

    cache_path = kagglehub.dataset_download(
        "olistbr/brazilian-ecommerce"
    )

    logger.info(
        f"Dataset downloaded to cache: {cache_path}"
    )

    target_dir = os.path.join(
        os.getcwd(),
        "data"
    )

    os.makedirs(
        target_dir,
        exist_ok=True
    )

    copied = 0

    logger.info(
        f"Copying files to: {target_dir}"
    )

    for file in os.listdir(cache_path):

        src = os.path.join(cache_path, file)
        dst = os.path.join(target_dir, file)

        if os.path.isfile(src):
            shutil.copy2(src, dst)
            copied += 1
            logger.info(f"Copied: {file}")

    logger.info(
        f"Download completed. "
        f"Total files copied: {copied}"
    )

    return target_dir