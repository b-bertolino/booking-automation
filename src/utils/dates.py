from datetime import date, timedelta


def get_booking_date() -> str:
    booking_date = date.today() + timedelta(days=8)
    return str(booking_date.day)