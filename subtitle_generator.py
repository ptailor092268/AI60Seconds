from pathlib import Path

SUBTITLE_DIR = Path("output/subtitles")
SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)


def clean_script_text(text):
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("(") and ")" in line:
            line = line.split(")", 1)[1].strip()

        line = line.replace("**", "")

        lines.append(line)

    return " ".join(lines)


def split_into_caption_chunks(text, words_per_caption=7):
    words = text.split()
    chunks = []

    for i in range(0, len(words), words_per_caption):
        chunks.append(" ".join(words[i:i + words_per_caption]))

    return chunks


def format_time(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)

    minutes = seconds // 60
    seconds = seconds % 60

    return f"00:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def create_srt(script_text, audio_duration, output_name):
    clean_text = clean_script_text(script_text)
    chunks = split_into_caption_chunks(clean_text)

    if not chunks:
        return None

    subtitle_path = SUBTITLE_DIR / f"{output_name}.srt"

    duration_per_chunk = audio_duration / len(chunks)

    with subtitle_path.open("w", encoding="utf-8") as file:
        for index, chunk in enumerate(chunks, start=1):
            start = (index - 1) * duration_per_chunk
            end = index * duration_per_chunk

            file.write(f"{index}\n")
            file.write(f"{format_time(start)} --> {format_time(end)}\n")
            file.write(f"{chunk}\n\n")

    return subtitle_path