import pdfplumber
import spacy
import re
from spacy.matcher import Matcher
from io import BytesIO



# Load Spacy NLP Model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts raw text from a PDF file using pdfplumber."""
    MAX_CHAR_LIMIT = 90000
    text = ""
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            if len(text) >= MAX_CHAR_LIMIT:
             break 
            text += page.extract_text() + "\n"
    return text.strip()

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


def extract_sentences_with_numeric_data(text):
    """Extracts key financial sentences with numeric data."""
    matcher = Matcher(nlp.vocab)

    matcher.add("MONEY_PATTERNS", [
        [{"LIKE_NUM": True}, {"TEXT": {"IN": ["$", "₹", "€", "£", "¥"]}}],
        [{"TEXT": {"IN": ["$", "₹", "€", "£", "¥"]}}, {"LIKE_NUM": True}],
        [{"TEXT": {"IN": ["$", "₹", "€", "£", "¥"]}}, {"IS_DIGIT": True}],
        [{"LIKE_NUM": True}, {"LOWER": {"IN": ["dollars", "rupees", "euros", "pounds", "yen"]}}],
        [{"LIKE_NUM": True}, {"LOWER": "rs"}, {"TEXT": {"REGEX": r"\.?"}}]
    ])

    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    page_number_pattern = re.compile(r'(\bpage\s*\d+\b)|(\bpg\.\s*\d+\b)|(\b\d+\s*/\s*\d+\b)|(\bpage\s*\d+\s*of\s*\d+\b)', flags=re.IGNORECASE)
    slash_word_pattern = re.compile(r'\b\w+/\w+\b')
    triple_slash_pattern = re.compile(r'\S*///\S*')

    doc = nlp(text)
    sentences_with_numeric_data = set()

    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME", "MONEY", "PERCENT"]:
            sentences_with_numeric_data.add(ent.sent.start)

    matches = matcher(doc)
    for match_id, start, end in matches:
        sent_index = doc[start].sent.start
        sentences_with_numeric_data.add(sent_index)

    number_pattern = re.compile(r'\b\d+\b|\b\d+[.,]\d+\b')
    for sent in doc.sents:
        if number_pattern.search(sent.text):
            sentences_with_numeric_data.add(sent.start)

    result = []
    for sent in doc.sents:
        if sent.start in sentences_with_numeric_data:
            clean_sentence = url_pattern.sub('', sent.text)
            clean_sentence = page_number_pattern.sub('', clean_sentence)
            clean_sentence = slash_word_pattern.sub('', clean_sentence)
            clean_sentence = triple_slash_pattern.sub('', clean_sentence)
            clean_sentence = clean_sentence.strip()
            if clean_sentence:
                result.append(clean_sentence)

    return " ".join(result)

