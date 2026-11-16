import pandas as pd
from src.logger import setup_logger

logger = setup_logger("ETL.Validate")

REQUIRED_COLUMNS = [
    "city",
    "latitude",
    "longitude",
    "temperature_c",
    "relative_humidity",
    "wind_speed",
    "measured_at",
    "extracted_at",
]


def validate_weather_data(df: pd.DataFrame) -> None:
    """Validate DataFrame schema, null values, and plausible meteorological ranges."""
    logger.info("Starting data quality validation...")

    if df.empty:
        raise ValueError("DataFrame is empty.")

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if any(df[col].isnull().any() for col in REQUIRED_COLUMNS):
        raise ValueError("Null values found in required columns.")

    if not df["temperature_c"].between(-90, 60).all():
        raise ValueError("Temperature out of plausible range (-90 to 60 C).")

    if not df["relative_humidity"].between(0, 100).all():
        raise ValueError("Relative humidity out of plausible range (0 to 100%).")

    if not df["wind_speed"].ge(0).all():
        raise ValueError("Wind speed cannot be negative.")

    logger.info("Validation completed: data approved.")