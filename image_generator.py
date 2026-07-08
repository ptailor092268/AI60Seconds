from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

IMAGE_DIR = Path("output/images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def generate_placeholder_image(prompt, output_name):
    width = 1080
    height = 1920

    image = Image.new("RGB", (width, height), (20, 30, 55))
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 64)
        body_font = ImageFont.truetype("arial.ttf", 42)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    draw.text(
        (60, 70),
        "AI60Seconds",
        fill="white",
        font=title_font
    )

    wrapped = textwrap.fill(prompt, width=24)

    draw.multiline_text(
        (60, 220),
        wrapped,
        fill="white",
        font=body_font,
        spacing=10
    )

    output = IMAGE_DIR / f"{output_name}.png"
    image.save(output)

    return output


if __name__ == "__main__":
    path = generate_placeholder_image(
        "Artificial Intelligence is changing the future.",
        "test_image"
    )

    print(path)