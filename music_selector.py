from pathlib import Path
import random

MUSIC_ROOT = Path("assets/music")


def choose_music_category(topic):
    topic_lower = topic.lower()

    if any(word in topic_lower for word in ["coding", "developer", "programming", "chatgpt", "gemini", "ai agent", "openai"]):
        return "Tech"

    if any(word in topic_lower for word in ["business", "startup", "money", "productivity", "work", "office"]):
        return "Corporate"

    if any(word in topic_lower for word in ["future", "breakthrough", "warning", "changed forever", "agi"]):
        return "Cinematic"

    if any(word in topic_lower for word in ["tools", "top", "best", "apps", "viral", "shorts"]):
        return "Energetic"

    if any(word in topic_lower for word in ["beginner", "learn", "simple", "daily", "focus"]):
        return "Calm"

    return "Tech"


def get_music_for_topic(topic):
    category = choose_music_category(topic)
    folder = MUSIC_ROOT / category

    tracks = list(folder.glob("*.mp3"))

    if not tracks:
        all_tracks = list(MUSIC_ROOT.glob("*/*.mp3"))
        if not all_tracks:
            return None
        return random.choice(all_tracks)

    return random.choice(tracks)


if __name__ == "__main__":
    test_topics = [
        "Top 5 AI tools for YouTube creators",
        "The future of AI is changing everything",
        "AI productivity hacks for daily work",
        "ChatGPT coding tips for beginners",
        "Simple AI tools for beginners"
    ]

    for topic in test_topics:
        music = get_music_for_topic(topic)
        print(f"{topic}")
        print(f"Selected: {music}")
        print()