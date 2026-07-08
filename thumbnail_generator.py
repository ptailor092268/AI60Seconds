from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

THUMBNAIL_DIR = Path("output/thumbnails")
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1280
HEIGHT = 720


def create_thumbnail(title, output_name):
    output_path = THUMBNAIL_DIR / f"{output_name}.png"

    image = Image.new("RGB", (WIDTH, HEIGHT), (15, 15, 30))
    draw = ImageDraw.Draw(image)

    try:
        font_big = ImageFont.truetype("arialbd.ttf", 72)
        font_small = ImageFont.truetype("arial.ttf", 36)
    except Exception:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(15, 15, 30))
    draw.rectangle((40, 40, WIDTH - 40, HEIGHT - 40), outline=(255, 255, 255), width=6)

    lines = textwrap.wrap(title, width=22)

    y = 170
    for line in lines[:4]:
        bbox = draw.textbbox((0, 0), line, font=font_big)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, y), line, font=font_big, fill=(255, 255, 255))
        y += 85

    badge_text = "AI IN 60 SECONDS"
    bbox = draw.textbbox((0, 0), badge_text, font=font_small)
    badge_width = bbox[2] - bbox[0]

    draw.rectangle((WIDTH - badge_width - 90, HEIGHT - 100, WIDTH - 40, HEIGHT - 40), fill=(255, 255, 255))
    draw.text((WIDTH - badge_width - 65, HEIGHT - 87), badge_text, font=font_small, fill=(15, 15, 30))

    image.save(output_path)

    return output_path


if __name__ == "__main__":
    path = create_thumbnail(
        "5 AI Tools That Save You Hours",
        "test_thumbnail"
    )

    print(f"Thumbnail created: {path}")