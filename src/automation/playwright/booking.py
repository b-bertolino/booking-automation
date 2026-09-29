from playwright.sync_api import sync_playwright
from domain.booking_result import BookingResult

import logging


logger = logging.getLogger(__name__)

def run_playwright(email: str, password: str, url: str, booking_day: str, booking_time: str) -> BookingResult:
    success = False
    error = None
    screen_path = ""
    # Avvia Playwright
    with sync_playwright() as p:
        # Lancia il browser visibile (headless=False) e rallentato (slow_mo)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        # context = browser.new_context() # Crea una nuova scheda (tab)
        try:
            page = browser.new_page()
            # page = context.new_page()

            logger.info("1. Atterraggio sulla pagina...")
            page.goto(url, wait_until="domcontentloaded")

            logger.info("2. Controllo presenza cookies...")
            cookie_btn = page.get_by_role("button", name="Rifiuta")
            if cookie_btn.is_visible(timeout=5000):
                cookie_btn.click()
                logger.info("2a. Cookies rifiutati!")
            else:
                logger.info("2a. Cookies non presenti!")

            logger.info("3. Inserimento credenziali...")
            page.locator("#UserName").fill(email)
            page.locator("#Password").fill(password)

            logger.info("4. Click sul bottone di accesso...")
            page.get_by_role("button", name="Login").click()

            logger.info("5. Accesso alle prenotazioni...")
            page.locator("#mainmenu-booking").click()
            page.locator("#side_booking_chooseActivity").click()
            page.get_by_text("SALA ATTREZZI").click()
            logger.info("5a. Selezione giorno...")
            page.locator('#btn-goto-date').click()
            day_slot = page.locator('td[class="day"]').get_by_text(booking_day, exact=True)
            if not day_slot.is_visible():
                page.locator(".datepicker-days th.next").click()
            day_slot.click()
            logger.info("5b. Selezione turno...")
            page.locator('.day-schedule').filter(has=page.locator('.day-schedule-label', has_text=booking_day)).locator('.event-slot.slot-available').filter(has=page.locator('.time-start', has_text=booking_time)).filter(has=page.locator('.slot-notes-before', has_text='Prenota')).click()
            page.locator('#btnConfirmAppointmentBooking').click()

            logger.info("6. Prenotazione terminata!")
            page.get_by_text("prenotazione confermata").is_visible(timeout=10000)
            screen_path = page.screenshot(path="artifacts/screenshots/booking_success.png")
            success = True
        except Exception as e:
            logger.error("Errore durante la prenotazione!")
            error = e
            screen_path = page.screenshot(path="artifacts/screenshots/booking_failure.png")
        finally:
            browser.close()
            return BookingResult(success, error, screen_path)