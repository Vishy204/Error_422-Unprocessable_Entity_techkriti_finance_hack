
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


#gpt story
def generate_story(summary):
    """Generates a financial story with twists and turns using ChatGPT API."""
    if not openai.api_key:
        print("Error: OpenAI API key not found.")
        return "API Key Missing"

    prompt = (
        "Here is the financial summary you need to convert into a story. Please ensure clarity, engagement, and an easy-to-follow structure while maintaining factual accuracy. Make sure to conclude with a well-reasoned outlook on the company’s future trajectory. "
        f"Summary: {summary}\n\nStory:"
    )

    try:
      system_message="""You are a skilled financial storyteller with the ability to break down complex financial data into engaging, easy-to-understand narratives. Your goal is to transform a given financial summary into a compelling story that explains key financial events, trends, and figures in a way that anyone—regardless of their financial background—can grasp.

Your story should be:

Engaging: Use an approachable tone, like a journalist explaining financial news to a general audience.

Simple & Clear: Avoid jargon when possible; when using technical terms, explain them in simple words.

Well-Structured: Start with an introduction that sets the stage, followed by a breakdown of key figures, trends, and their impact.

Relatable: Use analogies and real-world comparisons to make numbers and trends easier to grasp.

Forward-Looking: Provide insights into where the company is headed based on financial trends, market conditions, and strategic decisions. Predict potential risks and opportunities in a balanced manner.
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