from pathlib import Path
from moviepy import AudioFileClip, ColorClip, TextClip, CompositeVideoClip

VIDEO_DIR = Path("output/videos")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920


def read_srt(subtitle_path):
    captions = []

    if not subtitle_path or not Path(subtitle_path).exists():
        return captions

    content = Path(subtitle_path).read_text(encoding="utf-8")
    blocks = content.strip().split("\n\n")

    for block in blocks:
        lines = block.splitlines()

        if len(lines) >= 3:
            time_line = lines[1]
            text = " ".join(lines[2:])

            start_text, end_text = time_line.split(" --> ")
            start = srt_time_to_seconds(start_text)
            end = srt_time_to_seconds(end_text)

            captions.append((start, end, text))

    return captions


def srt_time_to_seconds(time_text):
    time_part, milliseconds = time_text.split(",")
    hours, minutes, seconds = time_part.split(":")

    return (
        int(hours) * 3600
        + int(minutes) * 60
        + int(seconds)
        + int(milliseconds) / 1000
    )


def build_video(audio_path, title, output_name, subtitle_path=None):
    audio = AudioFileClip(str(audio_path))
    duration = audio.duration

    background = ColorClip(
        size=(WIDTH, HEIGHT),
        color=(15, 15, 25),
        duration=duration
    )

    title_clip = TextClip(
        text=title,
        font_size=72,
        color="white",
        size=(950, None),
        method="caption"
    ).with_position(("center", 260)).with_duration(duration)

    clips = [background, title_clip]

    captions = read_srt(subtitle_path)

    for start, end, text in captions:
        caption_clip = TextClip(
            text=text,
            font_size=62,
            color="white",
            stroke_color="black",
            stroke_width=4,
            size=(950, None),
            method="caption"
        ).with_position(("center", 1250)).with_start(start).with_duration(end - start)

        clips.append(caption_clip)

    video = CompositeVideoClip(clips)
    video = video.with_audio(audio)

    output_path = VIDEO_DIR / f"{output_name}.mp4"

    video.write_videofile(
        str(output_path),
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    audio.close()
    video.close()

    return output_path


if __name__ == "__main__":
    test_audio = Path("output/audio/test.mp3")
    test_subtitles = Path("output/subtitles/test.srt")

    if not test_audio.exists():
        print("Missing output/audio/test.mp3. Run voice_generator.py first.")
    else:
        video_path = build_video(
            audio_path=test_audio,
            title="AI in 60 Seconds",
            output_name="test_video_captioned",
            subtitle_path=test_subtitles
        )
        print(f"Video created: {video_path}")