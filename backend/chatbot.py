

from pydantic import BaseModel

import os
from openai import OpenAI
import os
from huggingface_hub import login
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Configure OpenAI client to use Groq
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Specific finance-oriented model (small and lightweight)
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"  # Replace with a smaller LLaMA model if needed

class FinanceChatbot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def generate_response(self, query: str) -> str:
        if not GROQ_API_KEY:
            return "Sorry, the chatbot is currently unavailable."

        # Create a structured financial prompt
        financial_prompt = f"Please provide a small chat size response for '{query}' and use normal text not markdown"

        try:
            response = client.chat.completions.create(
                model="gemma2-9b-it",  
                messages=[{"role": "system", "content": "You are a helpful chatbot who get more questions on the financial side but balanced. IF questions asked financial based answer it in terms of company."},
                          {"role": "user", "content": financial_prompt}],
                max_tokens=200,
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I encountered an error processing your query."