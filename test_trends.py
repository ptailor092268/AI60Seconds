from trend_finder import get_trending_topics

print("\nTrending Topics\n")

topics = get_trending_topics()

for topic, score in topics:
    print(f"{topic:25} {score}")