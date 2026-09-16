from playwright.sync_api import sync_playwright
import time

def login_palestra():
    # Avvia Playwright
    with sync_playwright() as p:
        # Lancia il browser visibile (headless=False) e rallentato (slow_mo)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        # Crea una nuova scheda (tab)
        context = browser.new_context()
        page = context.new_page()

        print("1. Atterraggio sulla pagina di Sportrick...")
        page.goto("")

        print("2. Inserimento credenziali...")
        page.locator("input[id='UserName']").fill("Ciao")
        page.locator("input[id='Password']").fill("123")

        print("3. Click sul bottone di accesso...")
        page.locator("button[type='submit']", has_text="Login").click()

        print("Login effettuato! Attendo 5 secondi prima di chiudere...")
        # Aspettiamo un attimo per goderci la vista della dashboard loggata
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    login_palestra()