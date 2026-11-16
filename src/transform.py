import json
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

from src.logger import setup_logger
from src.paths import RAW_WEATHER_FILE

logger = setup_logger("ETL.Transform")


def transform_weather_data(json_filepath: str = RAW_WEATHER_FILE) -> pd.DataFrame:
    """Read raw JSON payload, extract current weather metrics, and return a clean DataFrame."""
    logger.info(f"Reading raw JSON file from '{json_filepath}'...")

    try:
        with open(json_filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Raw JSON file not found at '{json_filepath}'. Run extraction first.")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON file (corrupted or empty): {e}")
        raise

    current_weather = raw_data.get("current", {})

    transformed_data = {
        "city": ["Madrid"],
        "latitude": [raw_data.get("latitude")],
        "longitude": [raw_data.get("longitude")],
        "temperature_c": [current_weather.get("temperature_2m")],
        "relative_humidity": [current_weather.get("relative_humidity_2m")],
        "wind_speed": [current_weather.get("wind_speed_10m")],
        "measured_at": [current_weather.get("time")],
        "extracted_at": [datetime.now(ZoneInfo("Europe/Madrid")).strftime("%Y-%m-%d %H:%M:%S")],
    }

    df = pd.DataFrame(transformed_data)
    logger.info("Data transformation completed successfully.")
    logger.debug(f"Transformed data sample:\n{df.head()}")

    return df


if __name__ == "__main__":
    transform_weather_data()