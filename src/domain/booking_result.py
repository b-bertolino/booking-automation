from dataclasses import dataclass


@dataclass
class BookingResult:
    success: bool
    error: str | None = None
    screenshot_path: str | None = None