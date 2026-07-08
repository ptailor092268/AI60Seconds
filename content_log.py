import csv
from pathlib import Path

LOG_FILE = Path("output/content_log.csv")

def log_content(topic, filepath):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["topic", "file_path"])

        writer.writerow([topic, str(filepath)])