from dotenv import load_dotenv
from utils.dates import get_booking_date
from automation.playwright.booking import run_playwright
from time import perf_counter
from utils.logging_config import configure_logging
from utils.artifact_rotation_config import cleanup_old_directory, create_run_directory

import os, logging


logger = logging.getLogger(__name__)

def main():
    load_dotenv()

    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    url = os.getenv("URL")

    if not email or not password or not url:
        raise ValueError("Credenziali mancanti: imposta EMAIL e PASSWORD.")

    cleanup_old_directory(30)
    run_dir = create_run_directory()
    configure_logging(run_dir)

    booking_day = str(get_booking_date(8).day)
    booking_time = "20:15"

    start = perf_counter()
    run_playwright(email, password, url, booking_day, booking_time, run_dir)
    duration = perf_counter() - start
    logger.info(f"Tempo di esecuzione: {duration:.2f}s")

if __name__ == "__main__":
    main()