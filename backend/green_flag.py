
import os
from openai import OpenAI
import os

from dotenv import load_dotenv
import openai

load_dotenv()
GPT_API=os.getenv("GPT_KEY")
openai = OpenAI(api_key=GPT_API)
def generate_green(summary):
    """Generates a financial story with twists and turns using ChatGPT API."""
    if not openai.api_key:
        print("Error: OpenAI API key not found.")
        return "API Key Missing"

    prompt = (
        "Here is the financial summary: "
        f"Summary: {summary}\n\nRed flags: "
    )

    try:
      system_message="""You are a financial analyst tasked with identifying green flags—positive signs that indicate strong financial health, growth potential, or competitive advantages for a company. Your goal is to analyze the given financial summary while also leveraging pre-existing knowledge about the company to highlight strengths and opportunities. Stick to at max 5 points and give it in bullet points
"""
      user_prompt=prompt
      prompts = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
      ]
      completion = openai.chat.completions.create(model='gpt-4o-mini', messages=prompts)
      return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "Story generation failed."