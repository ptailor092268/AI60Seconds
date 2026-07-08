import argparse
from datetime import datetime
from pathlib import Path

from topics import get_topic
from script_generator import create_short_package
from content_log import log_content

OUTPUT_DIR = Path("output/scripts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="AI 60 Seconds YouTube Shorts Generator")
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    for i in range(1, args.count + 1):
        topic = get_topic()

        print(f"\n[{i}/{args.count}] Topic: {topic}")
        print("Generating content...")

        result = create_short_package(topic)

        filename = datetime.now().strftime(f"ai_short_{i}_%Y%m%d_%H%M%S.txt")
        filepath = OUTPUT_DIR / filename

        filepath.write_text(result, encoding="utf-8")

        log_content(topic, filepath)

        print(f"Saved: {filepath}")

    print("\nAll Shorts Generated Successfully!")


if __name__ == "__main__":
    main()