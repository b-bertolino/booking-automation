from dotenv import load_dotenv
from src.utils.dates import get_booking_date
from src.automation.playwright.booking import run_playwright
from time import perf_counter
from src.utils.logging_config import configure_logging
from src.utils.artifact_rotation_config import cleanup_old_directory, create_run_directory

import os, logging


logger = logging.getLogger(__name__)

def main():
    load_dotenv()

    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    url = os.getenv("URL")

    if not email or not password or not url:
        raise ValueError("Credenziali mancanti: imposta EMAIL, PASSWORD e URL.")

    cleanup_old_directory(14)
    run_dir = create_run_directory()
    configure_logging(run_dir)

    booking_date = get_booking_date()
    booking_time = os.getenv("TIME", "20:15")

    logger.info(f"Avvio prenotazione per {booking_date} alle {booking_time}!")

    start = perf_counter()
    run_playwright(email, password, url, str(booking_date.day), booking_time, run_dir)
    duration = perf_counter() - start
    logger.info(f"Tempo di esecuzione: {duration:.2f}s")

if __name__ == "__main__":
    main()