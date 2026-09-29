from datetime import date
from freezegun import freeze_time
from src.utils.dates import get_booking_date


@freeze_time("2026-05-10")
def test_get_booking_date_standard_offset():
    """Verifica il calcolo standard all'interno dello stesso mese (+8 giorni)."""
    result = get_booking_date(8)
    assert result == date(2026, 5, 18)


@freeze_time("2026-09-28")
def test_get_booking_date_month_rollover():
    """Verifica il salto corretto da settembre a ottobre."""
    result = get_booking_date(8)
    assert result == date(2026, 10, 6)
    assert result.day == 6
    assert result.month == 10


@freeze_time("2026-12-28")
def test_get_booking_date_year_rollover():
    """Verifica il passaggio da fine anno al nuovo anno."""
    result = get_booking_date(8)
    assert result == date(2027, 1, 5)
    assert result.year == 2027


def test_get_booking_date_zero_offset():
    """Verifica che con offset 0 restituisca la data odierna."""
    assert get_booking_date(0) == date.today()