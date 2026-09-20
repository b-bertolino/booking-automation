from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

def login_palestra():
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    if not email or not password:
        raise ValueError("Credenziali mancanti: imposta le variabili EMAIL e PASSWORD.")
    # Avvia Playwright
    with sync_playwright() as p:
        # Lancia il browser visibile (headless=False) e rallentato (slow_mo)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context() # Crea una nuova scheda (tab)
        page = context.new_page()

        print("1. Atterraggio sulla pagina di Sportrick...")
        page.goto("")

        print("2. Controllo presenza cookies..")
        cookie_btn = page.get_by_role("button", name="Rifiuta")
        if cookie_btn.is_visible(timeout=5000):
            cookie_btn.click()
            print("2a. Cookies rifiutati!")
        else:
            print("2a. Cookies non presenti!")

        print("3. Inserimento credenziali...")
        page.locator("input[id='UserName']").fill(email)
        page.locator("input[id='Password']").fill(password)

        print("4. Click sul bottone di accesso...")
        page.get_by_role("button", name="Login").click()

        print("5. Accesso alle prenotazioni...")
        page.locator("#mainmenu-booking").wait_for(timeout=5000, state='visible')
        page.locator("#mainmenu-booking").click()
        page.locator("#side_booking_chooseActivity").click()
        # page.locator("Nuova Prenotazione").wait_for(timeout=5000, state='visible')
        # page.locator("Nuova Prenotazione").click()
        # page.locator("SALA ATTREZZI")
        page.get_by_text("SALA ATTREZZI").click()
        browser.close()

if __name__ == "__main__":
    login_palestra()