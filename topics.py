import random
from trend_finder import get_trending_topics

FALLBACK_TOPICS = [
    "5 AI tools that save you time",
    "Best free AI websites for beginners",
    "How ChatGPT can help with daily work",
    "AI tools for YouTube creators",
    "AI tools for making videos"
]

def get_topic():
    trending = get_trending_topics()

    if trending:
        top_topics = [topic for topic, score in trending[:5]]
        return random.choice(top_topics)

    return random.choice(FALLBACK_TOPICS)