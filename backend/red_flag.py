
import openai
import os
from openai import OpenAI
import os
from huggingface_hub import login
from dotenv import load_dotenv
import openai

load_dotenv()
GPT_API=os.getenv("GPT_KEY")
openai = OpenAI(api_key=GPT_API)

def generate_red(summary):
    """Generates a financial story with twists and turns using ChatGPT API."""
    if not openai.api_key:
        print("Error: OpenAI API key not found.")
        return "API Key Missing"

    prompt = (
        "Here is the financial summary: "
        f"Summary: {summary}\n\nRed flags: "
    )

    try:
      system_message="""You are a financial risk analyst tasked with identifying potential red flags in a company’s financial summary. Your goal is to analyze the given financial data, leveraging both the provided summary and any pre-existing knowledge about the company to highlight concerns, risks, or warning signs. Stick to at max 5 points and give it in bullet points
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