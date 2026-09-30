from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

import logging


def configure_logging(run_dir: Path):
    file_handler = TimedRotatingFileHandler(
        filename=run_dir / "booking.log",
        # when="midnight",
        # interval=1,
        # backupCount=30,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            file_handler,
        ],
    )