import streamlit as st
import os
import re

# Debug – verify files exist
st.write("Files in data:", os.listdir("data") if os.path.exists("data") else "Folder not found")

# -----------------------------
# PDF LOADER (WORKS ON STREAMLIT CLOUD)
# -----------------------------
from llama_index.readers.file import PDFReader
from llama_index.core import VectorStoreIndex, Settings

Settings.llm = None
Settings.embed_model = None   # No embeddings

DATA_DIR = "data"

# Ensure data directory exists
if not os.path.isdir(DATA_DIR):
    st.error("❌ 'data/' folder is missing in the repository. Create it and add PDF files.")
    st.stop()

# ------------------------------------------------------
# PREDEFINED Q&A
# ------------------------------------------------------
PREDEFINED_QA = {
    "training programs": """- AI/ML
- Data Analytics
- DevOps
- Cloud Computing
- Web/Mobile Development
- Full Stack Development
- Cybersecurity & Networking
- IT staffing
- IT Managed Services
- Corporate Training
- Rookie Training Programs
- Internships
- Placement Support
- Interview Preparation""",

    "key features": """- Flipped Classroom Model
- Omnichannel Learning (Online + Offline)
- Modern labs with study rooms
- Knowledge banks for self-paced learning""",

    "experience": "Founded in 1999 — 26 years (as of 2025).",

    "what makes rooman different": """- India's only Omnichannel Training Institute (claimed)
- Uses Flipped Classroom Model for online training
- 1.2M+ students empowered
- 100+ physical centers across India""",

    "locations": """- Presence in 52 cities
- 198 training centers
- Major city: Bangalore""",

    "partners": """- 24 Academic Partners
- Kuvempu University programs (BSc-IT, MSc-IT IMS)
- Government partnerships for skilling & reskilling"""
}

def check_predefined_answers(query):
    q = query.lower()

    if any(word in q for word in ["training program", "courses offered", "what courses"]):
        return PREDEFINED_QA["training programs"]
    if any(word in q for word in ["key feature", "training approach", "features"]):
        return PREDEFINED_QA["key features"]
    if any(word in q for word in ["experience", "years", "established"]):
        return PREDEFINED_QA["experience"]
    if any(word in q for word in ["different", "unique", "why rooman"]):
        return PREDEFINED_QA["what makes rooman different"]
    if any(word in q for word in ["location", "branch", "city", "center"]):
        return PREDEFINED_QA["locations"]
    if "partner" in q or "university" in q:
        return PREDEFINED_QA["partners"]

    return None


# -----------------------------
# LOAD DOCUMENTS (PDFReader)
# -----------------------------
@st.cache_resource(show_spinner=True)
def load_docs():
    pdf_loader = PDFReader()
    docs = []

    for file in os.listdir(DATA_DIR):
        if file.lower().endswith(".pdf"):
            path = os.path.join(DATA_DIR, file)
            pdf_docs = pdf_loader.load_data(path)
            docs.extend(pdf_docs)

    return docs


DOCUMENTS = load_docs()

if not DOCUMENTS:
    st.error("❌ No readable PDF files found inside data/. Upload a valid PDF.")
    st.stop()

# Keyword search (very fast)
def keyword_retrieval(query):
    q = query.lower()
    matches = []

    for d in DOCUMENTS:
        text = d.text.lower()
        if q in text:
            matches.append(d.text[:2000])

    if matches:
        return "\n\n---\n\n".join(matches)

    return "No relevant information found."


# UI
st.title("🤖 Rooman Knowledge Assistant")

user_query = st.text_input("Ask the Rooman Knowledge Assistant:")

if user_query:
    faq = check_predefined_answers(user_query)

    if faq:
        answer = faq
    else:
        with st.spinner("Searching your documents..."):
            raw = keyword_retrieval(user_query)
        answer = raw

    st.subheader("Answer:")
    st.markdown(answer)
