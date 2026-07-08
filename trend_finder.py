from pytrends.request import TrendReq


def get_trending_topics():

    pytrends = TrendReq(hl="en-US", tz=360)

    keywords = [
        "ChatGPT",
        "Google Gemini",
        "OpenAI",
        "Claude AI",
        "Perplexity AI",
        "Midjourney",
        "Runway AI",
        "Microsoft Copilot",
        "AI Agents",
        "AI Tools"
    ]

    results = []

    for keyword in keywords:

        try:

            pytrends.build_payload([keyword], timeframe="today 3-m")

            df = pytrends.interest_over_time()

            if not df.empty:

                score = int(df[keyword].iloc[-1])

                results.append((keyword, score))

        except Exception:

            pass

    results.sort(key=lambda x: x[1], reverse=True)

    return results