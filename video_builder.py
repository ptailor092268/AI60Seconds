from pathlib import Path
from moviepy import AudioFileClip, ColorClip, TextClip, CompositeVideoClip

VIDEO_DIR = Path("output/videos")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920


def build_video(audio_path, title, output_name):
    audio = AudioFileClip(str(audio_path))
    duration = audio.duration

    background = ColorClip(
        size=(WIDTH, HEIGHT),
        color=(15, 15, 25),
        duration=duration
    )

    title_clip = TextClip(
        text=title,
        font_size=80,
        color="white",
        size=(950, None),
        method="caption"
    ).with_position(("center", "center")).with_duration(duration)

    video = CompositeVideoClip([background, title_clip])
    video = video.with_audio(audio)

    output_path = VIDEO_DIR / f"{output_name}.mp4"

    video.write_videofile(
        str(output_path),
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path


if __name__ == "__main__":
    test_audio = Path("output/audio/test.mp3")

    if not test_audio.exists():
        print("Missing output/audio/test.mp3. Run voice_generator.py first.")
    else:
        video_path = build_video(
            test_audio,
            "AI in 60 Seconds",
            "test_video"
        )
        print(f"Video created: {video_path}")