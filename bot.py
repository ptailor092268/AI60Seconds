import argparse
from datetime import datetime
from pathlib import Path

from topics import get_topic
from script_generator import create_short_package
from content_log import log_content
from voice_generator import generate_voice

SCRIPT_DIR = Path("output/scripts")
AUDIO_DIR = Path("output/audio")

SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def extract_script_text(full_content):
    if "SCRIPT:" in full_content:
        script_part = full_content.split("SCRIPT:", 1)[1]

        if "DESCRIPTION:" in script_part:
            script_part = script_part.split("DESCRIPTION:", 1)[0]

        return script_part.strip()

    return full_content.strip()


def main():
    parser = argparse.ArgumentParser(description="AI60Seconds YouTube Shorts Generator")
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    for i in range(1, args.count + 1):
        topic = get_topic()

        print(f"\n[{i}/{args.count}] Topic: {topic}")
        print("Generating script package...")

        result = create_short_package(topic)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"ai_short_{i}_{timestamp}"

        script_path = SCRIPT_DIR / f"{base_name}.txt"
        script_path.write_text(result, encoding="utf-8")

        print("Generating voiceover...")
        voice_text = extract_script_text(result)
        generate_voice(voice_text, base_name)

        log_content(topic, script_path)

        print(f"Saved script: {script_path}")
        print(f"Saved audio: output/audio/{base_name}.mp3")

    print("\nAll Shorts Generated Successfully!")


if __name__ == "__main__":
    main()