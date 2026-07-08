from ai_client import generate_text

def create_short_package(topic: str) -> str:
    prompt = f"""
Create a YouTube Shorts package for the topic: {topic}

Return exactly this format:

TITLE:
A viral YouTube Shorts title

SCRIPT:
A 45-60 second spoken script with a strong hook, simple explanation, and strong ending.

DESCRIPTION:
A short YouTube description.

HASHTAGS:
10 relevant hashtags.

THUMBNAIL PROMPT:
A clear AI image prompt for a YouTube Shorts thumbnail.
"""
    return generate_text(prompt)