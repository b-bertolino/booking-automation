from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


def get_booking_date() -> date:
    today = datetime.now(ZoneInfo("Europe/Rome")).date()
    return today + timedelta(days=8)
    