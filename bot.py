import argparse
from datetime import datetime
from pathlib import Path
from moviepy import AudioFileClip

from topics import get_topic
from script_generator import create_short_package
from content_log import log_content
from voice_generator import generate_voice
from video_builder import build_video
from subtitle_generator import create_srt

SCRIPT_DIR = Path("output/scripts")
AUDIO_DIR = Path("output/audio")
VIDEO_DIR = Path("output/videos")
SUBTITLE_DIR = Path("output/subtitles")

SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)


def extract_section(full_content, start_label, end_label=None):
    if start_label not in full_content:
        return ""

    text = full_content.split(start_label, 1)[1]

    if end_label and end_label in text:
        text = text.split(end_label, 1)[0]

    return text.strip()


def extract_title(full_content):
    title = extract_section(full_content, "TITLE:", "SCRIPT:")
    return title if title else "AI in 60 Seconds"


def extract_script_text(full_content):
    script = extract_section(full_content, "SCRIPT:", "DESCRIPTION:")
    return script if script else full_content.strip()


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
        audio_path = AUDIO_DIR / f"{base_name}.mp3"

        script_path.write_text(result, encoding="utf-8")

        title = extract_title(result)
        voice_text = extract_script_text(result)

        print("Generating voiceover...")
        generate_voice(voice_text, base_name)

        print("Creating subtitle file...")
        audio = AudioFileClip(str(audio_path))
        subtitle_path = create_srt(
            script_text=voice_text,
            audio_duration=audio.duration,
            output_name=base_name
        )
        audio.close()

        print("Building video with captions...")
        video_path = build_video(
            audio_path=audio_path,
            title=title,
            output_name=base_name,
            subtitle_path=subtitle_path
        )

        log_content(topic, script_path)

        print(f"Saved script: {script_path}")
        print(f"Saved audio: {audio_path}")
        print(f"Saved subtitles: {subtitle_path}")
        print(f"Saved video: {video_path}")

    print("\nAll Shorts Generated Successfully!")


if __name__ == "__main__":
    main()