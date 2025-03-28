
from transformers import pipeline 


# Load Transformer Model for Summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def chunk_text(text, tokenizer, max_tokens=512):
    """Split text into smaller chunks for summarization."""
    inputs = tokenizer(text, return_tensors="pt", truncation=False)
    input_ids = inputs["input_ids"][0]

    chunks = []
    for i in range(0, len(input_ids), max_tokens):
        chunk_ids = input_ids[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)

    return chunks


def summarize_text(text, max_tokens=512):
    """Summarizes extracted financial data."""
    tokenizer = summarizer.tokenizer
    chunks = chunk_text(text, tokenizer, max_tokens=max_tokens)
    summaries = []

    for chunk in chunks:
        summary = summarizer(chunk, max_length=80, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)

    return " ".join(summaries)