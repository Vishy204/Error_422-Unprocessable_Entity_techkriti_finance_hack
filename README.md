# Error 422- Unprocessable Entity

## Overview
This project is designed to automate financial story generation from company reports using AI. It extracts relevant financial data, summarizes the company's performance, and generates a narrative using a fine-tuned model. The system also retrieves external financial data and news to provide a comprehensive analysis.

**Important:** This system is designed to work for **any company in India** and is **not limited to just three companies as mentioned in the original problem statement.**

## Demo Video
A demo video showcasing the complete workflow is available [here](#) (Upload your video link here).

## Workflow
### 1. **Upload Annual Report**
- Users upload the annual financial report of any company through a web interface.

### 2. **Text Extraction & Preprocessing**
- **PDFPlumber** extracts text from the uploaded PDF.
- **spaCy** processes the extracted text and identifies key financial entities using Named Entity Recognition (NER).

### 3. **External Data Retrieval**
- The extracted company name is used to fetch financial data (Balance Sheets, Income Statements, and Cash Flow) from **Yahoo Finance**.
- Relevant financial news is retrieved from **Google News**.

### 4. **Financial Summarization**
- A summarization model processes the extracted and retrieved data to generate an overview of the company’s financial performance for the year.

### 5. **Story Generation**
- A **fine-tuned Frontier model** generates a compelling financial story based on the summarized data.

### 6. **Sentiment Analysis & Comparison**
- The system compares the sentiment of the generated story with extracted news articles.
- Graphs and visuals are created to highlight key insights.

### 7. **User Interface & Output**
- Users receive a detailed financial story along with visualized insights for better understanding.

## How to Use
1. Upload the annual report of a company in PDF format.
2. The system processes the report, retrieves additional data, and generates a financial story.
3. Gives a comparison of the generated story with real-world news sentiment analysis.
4. View graphs and insights for better financial understanding.

## Workflow Image
![Workflow](Screenshot_2025-03-28_at_8.14.55_AM.png)

## Contributions
Feel free to raise issues or contribute to improving the model and expanding its capabilities!

## License
This project is open-source and available under the [MIT License](LICENSE).
