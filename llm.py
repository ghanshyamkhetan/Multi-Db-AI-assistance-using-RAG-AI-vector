from google import genai
from config import GOOGLE_API_KEY

client = genai.Client(
    api_key=GOOGLE_API_KEY
)


def ask_llm(prompt):

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text