import asyncio
import edge_tts
import os

VOICE = "en-US-AndrewNeural"

OUTPUT_FOLDER = "output/audio"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


async def create_voice(text, filename):
    communicate = edge_tts.Communicate(text, VOICE)

    await communicate.save(
        os.path.join(
            OUTPUT_FOLDER,
            filename + ".mp3"
        )
    )


def generate_voice(script, filename):

    asyncio.run(
        create_voice(script, filename)
    )


if __name__ == "__main__":

    sample = """
Welcome to AI in 60 Seconds.

Today we're talking about the newest AI breakthrough.

Don't forget to subscribe for daily AI updates.
"""

    generate_voice(sample, "test")

    print("Voice created successfully!")