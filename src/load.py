import os
import pandas as pd

from src.logger import setup_logger
from src.paths import PROCESSED_WEATHER_FILE

logger = setup_logger("ETL.Load")


def load_weather_data(df: pd.DataFrame, output_filepath: str = PROCESSED_WEATHER_FILE) -> None:
    """Idempotently append transformed weather records to the historical CSV file."""
    logger.info("Starting data load...")

    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    file_exists = os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 0

    if file_exists:
        existing_records = pd.read_csv(output_filepath, usecols=["measured_at"])
        if df["measured_at"].iloc[0] in existing_records["measured_at"].values:
            logger.info("Measurement timestamp already exists in CSV. Skipping load.")
            return

    try:
        df.to_csv(
            output_filepath,
            mode="a",
            index=False,
            header=not file_exists,
            encoding="utf-8",
        )
        logger.info(f"Data successfully loaded into '{output_filepath}'.")
    except Exception as e:
        logger.error(f"Critical error writing CSV file: {e}")
        raise


if __name__ == "__main__":
    from src.transform import transform_weather_data

    df_test = transform_weather_data()
    load_weather_data(df_test)