from pathlib import Path
import numpy as np
from moviepy import AudioFileClip, TextClip, CompositeVideoClip, VideoClip, ImageClip

VIDEO_DIR = Path("output/videos")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920


def srt_time_to_seconds(time_text):
    time_part, milliseconds = time_text.split(",")
    hours, minutes, seconds = time_part.split(":")

    return (
        int(hours) * 3600
        + int(minutes) * 60
        + int(seconds)
        + int(milliseconds) / 1000
    )


def read_srt(subtitle_path):
    captions = []

    if not subtitle_path or not Path(subtitle_path).exists():
        return captions

    content = Path(subtitle_path).read_text(encoding="utf-8")
    blocks = content.strip().split("\n\n")

    for block in blocks:
        lines = block.splitlines()

        if len(lines) >= 3:
            start_text, end_text = lines[1].split(" --> ")
            text = " ".join(lines[2:])

            captions.append(
                (
                    srt_time_to_seconds(start_text),
                    srt_time_to_seconds(end_text),
                    text,
                )
            )

    return captions


def create_animated_background(duration):
    def make_frame(t):
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        for y in range(HEIGHT):
            blue = int(30 + 40 * np.sin((y / 180) + t))
            purple = int(35 + 35 * np.cos((y / 240) + t))
            frame[y, :, 0] = 15
            frame[y, :, 1] = purple
            frame[y, :, 2] = blue + 50

        return frame

    return VideoClip(make_frame, duration=duration)


def create_progress_bar(duration):
    def make_frame(t):
        frame = np.zeros((20, WIDTH, 3), dtype=np.uint8)
        progress_width = int((t / duration) * WIDTH)

        frame[:, :progress_width, :] = [255, 255, 255]
        frame[:, progress_width:, :] = [60, 60, 80]

        return frame

    return VideoClip(make_frame, duration=duration).with_position(("center", HEIGHT - 40))


def create_image_clip(image_path, duration):
    if not image_path or not Path(image_path).exists():
        return None

    clip = ImageClip(str(image_path)).with_duration(duration)

    clip = clip.resized(height=HEIGHT)

    if clip.w < WIDTH:
        clip = clip.resized(width=WIDTH)

    clip = clip.cropped(
        x_center=clip.w / 2,
        y_center=clip.h / 2,
        width=WIDTH,
        height=HEIGHT
    )

    return clip.with_position(("center", "center"))


def build_video(audio_path, title, output_name, subtitle_path=None, image_path=None):
    audio = AudioFileClip(str(audio_path))
    duration = audio.duration

    image_clip = create_image_clip(image_path, duration)

    if image_clip:
        background = image_clip
    else:
        background = create_animated_background(duration)

    progress_bar = create_progress_bar(duration)

    title_clip = TextClip(
        text=title,
        font_size=70,
        color="white",
        stroke_color="black",
        stroke_width=3,
        size=(950, None),
        method="caption"
    ).with_position(("center", 220)).with_duration(duration)

    clips = [background, title_clip, progress_bar]

    captions = read_srt(subtitle_path)

    for start, end, text in captions:
        caption_clip = TextClip(
            text=text,
            font_size=64,
            color="white",
            stroke_color="black",
            stroke_width=5,
            size=(950, None),
            method="caption"
        ).with_position(("center", 1240)).with_start(start).with_duration(end - start)

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