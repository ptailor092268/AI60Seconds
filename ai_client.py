import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()


def generate_text(prompt):

    if AI_PROVIDER == "gemini":
        from google import genai

        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text


    elif AI_PROVIDER == "openai":

        from openai import OpenAI

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text


    else:

        raise Exception("Unsupported AI Provider")