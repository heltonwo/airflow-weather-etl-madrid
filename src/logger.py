import logging
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_logger(name: str, log_file: str = "logs/etl_pipeline.log") -> logging.Logger:
    """Configure and return a standardized logger writing to both console and file."""
    log_file = os.path.join(project_root, log_file)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger