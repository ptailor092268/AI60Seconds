from pathlib import Path
import json

PACKAGE_DIR = Path("output/upload_packages")
PACKAGE_DIR.mkdir(parents=True, exist_ok=True)


def extract_section(full_content, start_label, end_label=None):
    if start_label not in full_content:
        return ""

    text = full_content.split(start_label, 1)[1]

    if end_label and end_label in text:
        text = text.split(end_label, 1)[0]

    return text.strip()


def create_upload_package(full_content, video_path, thumbnail_path, output_name):
    title = extract_section(full_content, "TITLE:", "SCRIPT:")
    description = extract_section(full_content, "DESCRIPTION:", "HASHTAGS:")
    hashtags = extract_section(full_content, "HASHTAGS:", "THUMBNAIL PROMPT:")

    package = {
        "title": title,
        "description": description,
        "hashtags": hashtags,
        "video_path": str(video_path),
        "thumbnail_path": str(thumbnail_path)
    }

    output_path = PACKAGE_DIR / f"{output_name}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(package, file, indent=4)

    return output_path