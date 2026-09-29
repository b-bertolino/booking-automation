from dotenv import load_dotenv
from utils.dates import get_booking_date
from automation.playwright.booking import run_playwright

import os


def main():
    load_dotenv()

    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    url = os.getenv("URL")

    if not email or not password or not url:
        raise ValueError("Credenziali mancanti: imposta EMAIL e PASSWORD.")

    booking_day = str(get_booking_date(8).day)
    booking_time = "18:15"

    run_playwright(email, password, url, booking_day, booking_time)

if __name__ == "__main__":
    main()