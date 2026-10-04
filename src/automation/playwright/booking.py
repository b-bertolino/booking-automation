from playwright.sync_api import sync_playwright, Page
from src.domain.booking_result import BookingResult

import logging, os

logger = logging.getLogger(__name__)
headless = os.getenv("HEADLESS", "false").lower() == "true"


from pathlib import Path


def take_screenshot(page: Page, result: str, run_dir: Path) -> str:
    path = run_dir / f"booking_{result}.png"

    page.screenshot(path=str(path))

    return str(path)

# AGGIUNTIVI DA VERIFICARE
def highlight(locator):
    locator.scroll_into_view_if_needed()

    locator.evaluate(
        """element => {
            element.dataset.originalOutline = element.style.outline;
            element.dataset.originalBackground = element.style.backgroundColor;

            element.style.outline = "4px solid red";
            element.style.backgroundColor = "yellow";
        }"""
    )

# AGGIUNTIVI DA VERIFICARE
def remove_highlight(locator):
    locator.evaluate(
        """element => {
            element.style.outline = element.dataset.originalOutline || "";
            element.style.backgroundColor = element.dataset.originalBackground || "";

            delete element.dataset.originalOutline;
            delete element.dataset.originalBackground;
        }"""
    )


def run_playwright(email: str, password: str, url: str, booking_day: str, booking_time: str, run_dir: Path) -> BookingResult:
    success = False
    error = None
    screen_path = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=1000)
        # context = browser.new_context() # Crea una nuova scheda (tab)
        try:
            page = browser.new_page()
            # page = context.new_page()

            logger.info("Atterraggio sulla pagina")
            page.goto(url, wait_until="domcontentloaded")

            logger.info("Controllo presenza cookies")
            cookie_btn = page.get_by_role("button", name="Rifiuta")
            if cookie_btn.is_visible(timeout=5000):
                cookie_btn.click()
                logger.info("Cookies rifiutati!")
            else:
                logger.info("Cookies non presenti!")

            logger.info("Inserimento credenziali")
            page.locator("#UserName").fill(email)
            page.locator("#Password").fill(password)

            logger.info("Click sul bottone di accesso")
            page.get_by_role("button", name="Login").click()

            logger.info("Accesso alle prenotazioni")
            page.locator("#mainmenu-booking").click()
            page.locator("#side_booking_chooseActivity").click()
            page.get_by_text("SALA ATTREZZI").click()
            logger.info("Selezione giorno")
            page.locator('#btn-goto-date').click()
            day_slot = page.locator('td[class="day"]').get_by_text(booking_day, exact=True)
            if not day_slot.is_visible():
                page.locator(".datepicker-days th.next").click()
            day_slot.click()
            logger.info("Selezione turno")
            page.locator('.day-schedule').filter(has=page.locator('.day-schedule-label', has_text=booking_day)).locator('.event-slot.slot-available').filter(has=page.locator('.time-start', has_text=booking_time)).scroll_into_view_if_needed()
            page.locator('.day-schedule').filter(has=page.locator('.day-schedule-label', has_text=booking_day)).locator('.event-slot.slot-available').filter(has=page.locator('.time-start', has_text=booking_time)).filter(has=page.locator('.slot-notes-before', has_text='Prenota')).click()
            page.locator('#btnConfirmAppointmentBooking').click()

            page.get_by_text("prenotazione confermata").is_visible(timeout=10000)
            logger.info("Prenotazione terminata con successo!")
            # screen_path = page.screenshot(path="artifacts/screenshots/booking_success.png")
            screen_path = take_screenshot(page, "success", run_dir)
            success = True
        except Exception:
            logger.exception("Errore durante la prenotazione!")
            # screen_path = page.screenshot(path="artifacts/screenshots/booking_failure.png")
            screen_path = take_screenshot(page, "failure", run_dir)
        finally:
            browser.close()

    return BookingResult(success, error, screen_path)