import logging
import os


os.makedirs("logs", exist_ok=True)


logging.basicConfig(
    filename="logs/validation_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_validation_failure(attempt: int, error: str):
    logging.error(
        f"Validation failed on attempt {attempt}: {error}"
    )