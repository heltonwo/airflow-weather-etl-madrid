from src.extract import extract_weather_data
from src.load import load_weather_data
from src.logger import setup_logger
from src.transform import transform_weather_data
from src.validate import validate_weather_data

logger = setup_logger("ETL.Main")


def run_etl_pipeline() -> None:
    """Execute the complete local Weather ETL pipeline sequentially."""
    logger.info("=== STARTING WEATHER ETL PIPELINE ===")

    try:
        extract_weather_data()
        df_processed = transform_weather_data()
        validate_weather_data(df_processed)
        load_weather_data(df_processed)
        logger.info("=== WEATHER ETL PIPELINE COMPLETED SUCCESSFULLY ===")
    except Exception as e:
        logger.critical(f"ETL pipeline failed due to a critical error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    run_etl_pipeline()