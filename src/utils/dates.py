from datetime import date, timedelta


def get_booking_date() -> date:
    return date.today() + timedelta(days=8)
    