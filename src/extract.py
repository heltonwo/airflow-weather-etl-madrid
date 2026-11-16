import json
import os
import requests

from src.logger import setup_logger
from src.paths import DATA_RAW_DIR, RAW_WEATHER_FILE

logger = setup_logger("ETL.Extract")


def extract_weather_data() -> None:
    """Fetch current weather data for Madrid from Open-Meteo API and save raw JSON."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 40.4168,
        "longitude": -3.7038,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "Europe/Madrid",
    }
    logger.info("Sending HTTP request to Open-Meteo API...")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Critical error during API request: {e}")
        raise

    raw_data = response.json()
    logger.info("Raw weather data successfully retrieved from API.")

    os.makedirs(DATA_RAW_DIR, exist_ok=True)
    with open(RAW_WEATHER_FILE, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=4)

    logger.info(f"Raw payload saved successfully to '{RAW_WEATHER_FILE}'.")


if __name__ == "__main__":
    extract_weather_data()