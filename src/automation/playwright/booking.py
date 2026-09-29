from playwright.sync_api import sync_playwright


def run_playwright(email: str, password: str, url: str, booking_day: str, booking_time: str):
    # Avvia Playwright
    with sync_playwright() as p:
        # Lancia il browser visibile (headless=False) e rallentato (slow_mo)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        # context = browser.new_context() # Crea una nuova scheda (tab)
        try:
            page = browser.new_page()
            # page = context.new_page()

            print("1. Atterraggio sulla pagina di Sportrick...")
            page.goto(url, wait_until="domcontentloaded")

            print("2. Controllo presenza cookies...")
            cookie_btn = page.get_by_role("button", name="Rifiuta")
            if cookie_btn.is_visible(timeout=5000):
                cookie_btn.click()
                print("\t2a. Cookies rifiutati!")
            else:
                print("\t2a. Cookies non presenti!")

            print("3. Inserimento credenziali...")
            page.locator("#UserName").fill(email)
            page.locator("#Password").fill(password)

            print("4. Click sul bottone di accesso...")
            page.get_by_role("button", name="Login").click()

            print("5. Accesso alle prenotazioni...")
            page.locator("#mainmenu-booking").click()
            page.locator("#side_booking_chooseActivity").click()
            page.get_by_text("SALA ATTREZZI").click()
            print("\t5a. Selezione giorno...")
            page.locator('#btn-goto-date').click()
            day_slot = page.locator('td[class="day"]').get_by_text(booking_day, exact=True)
            if not day_slot.is_visible():
                page.locator(".datepicker-days th.next").click()
            day_slot.click()
            print("\t5b. Selezione turno...")
            page.locator('.day-schedule').filter(has=page.locator('.day-schedule-label', has_text=booking_day)).locator('.event-slot.slot-available').filter(has=page.locator('.time-start', has_text=booking_time)).filter(has=page.locator('.slot-notes-before', has_text='Prenota')).click()
            page.locator('#btnConfirmAppointmentBooking').click()

            print("6. Prenotazione terminata!")
            page.get_by_text("prenotazione confermata").is_visible(timeout=10000)
            page.screenshot(path="artifacts/screenshots/booking_success.png")
        except Exception as e:
            print(f"Qualcosa è andato storto durante la prenotazione:\n{e}")
            page.screenshot(path="artifacts/screenshots/booking_failure.png")
        finally:
            browser.close()