
from fastapi import FastAPI, File, UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel






from utils import extract_text_from_pdf, extract_sentences_with_numeric_data, chunk_text
from summary_model import summarize_text
from chatbot import FinanceChatbot
from red_flag import generate_red
from green_flag import generate_green
from story import generate_story
from web_scraper import extract_company_name,get_financial_news_titles,analyze_financial_summary,compare_sentiments
from visualisation import extract_comp_name,fetch_financial_data,process_income_statement,process_balance_sheet,plot_financial_data


# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """Handles PDF upload, extracts text, processes it, and returns a summarized result."""
    pdf_bytes = await file.read()
    raw_text = extract_text_from_pdf(pdf_bytes)
    extracted_text = extract_sentences_with_numeric_data(raw_text)
    summary = summarize_text(extracted_text)
    financial_story = generate_story(summary)
    green_flags = generate_green(summary)
    red_flags = generate_red(summary)
    comp_name= extract_company_name(summary)
    news_titles ,news_score= get_financial_news_titles(comp_name)
    summary_sentiment, summary_confidence = analyze_financial_summary(summary)
    conclusion = compare_sentiments(summary, news_score)

    comp_name=extract_comp_name(summary)
    financial_data = fetch_financial_data(comp_name)
    process_balance_sheet()
    process_income_statement()
    visualisation=plot_financial_data("cleaned_income_statement.csv","cleaned_balance_sheet.csv")


    

    
    return {
        "summary": summary,
        "redFlags": red_flags,
        "greenFlags": green_flags,
        "story": financial_story,
        "conclusion": conclusion,
        "visualisation": "hi,"
    }

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

finance_chatbot = FinanceChatbot()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    try:
        response_text = await finance_chatbot.generate_response(chat_message.message)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
