from datetime import datetime, timedelta
from pathlib import Path

import shutil


ARTIFACTS_DIR = Path("artifacts")

def create_run_directory() -> Path:
    now = datetime.now()

    run_dir = (
        ARTIFACTS_DIR
        / now.strftime("%Y-%m-%d")
        / now.strftime("%H:%M:%S")
    )

    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

def cleanup_old_directory(retention_days: int = 30) -> None:
    if not ARTIFACTS_DIR.exists():
        return

    cutoff = datetime.now() - timedelta(days=retention_days)

    for date_dir in ARTIFACTS_DIR.iterdir():
        if not date_dir.is_dir():
            continue

        try:
            date = datetime.strptime(date_dir.name, "%Y-%m-%d")
        except ValueError:
            continue

        if date < cutoff:
            shutil.rmtree(date_dir)