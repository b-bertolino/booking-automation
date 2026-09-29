from datetime import date, timedelta


def get_booking_date(days_from_today: int) -> date:
    return date.today() + timedelta(days=days_from_today)