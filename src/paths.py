
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

RAW_WEATHER_FILE = os.path.join(DATA_RAW_DIR, "weather_raw.json")
PROCESSED_WEATHER_FILE = os.path.join(
    DATA_PROCESSED_DIR,
    "weather_data_processed.csv"
)
