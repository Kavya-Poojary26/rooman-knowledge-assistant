import streamlit as st
import os
import re

# LlamaIndex imports (NO embeddings, NO LLM)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

# -----------------------------
# RETRIEVAL-ONLY MODE
# -----------------------------
Settings.llm = None
Settings.embed_model = None   # No embedding model

# Ensure data folder exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Debug – show files found
st.write("Files in data:", os.listdir(DATA_DIR) if os.path.exists(DATA_DIR) else "Folder not found")

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
- Large scale: 1.2M+ students empowered
- 100+ physical centers across India""",

    "locations": """- Presence in 52 cities
- 198 training centers
- Major city: Bangalore""",

    "partners": """- 24 Academic Partners
- Kuvempu University programs (BSc-IT, MSc-IT IMS)
- Government partnerships for skilling & reskilling"""
}

# ------------------------------------------------------
# CHECK FOR PREDEFINED ANSWERS FIRST
# ------------------------------------------------------
def check_predefined_answers(query):
    q = query.lower()

    if any(word in q for word in ["training program", "courses offered", "what courses"]):
        return PREDEFINED_QA["training programs"]

    if any(word in q for word in ["key feature", "training approach", "features"]):
        return PREDEFINED_QA["key features"]

    if any(word in q for word in ["experience", "how many years", "years", "established"]):
        return PREDEFINED_QA["experience"]

    if any(word in q for word in ["different", "unique", "why rooman"]):
        return PREDEFINED_QA["what makes rooman different"]

    if any(word in q for word in ["location", "branch", "city", "center"]):
        return PREDEFINED_QA["locations"]

    if "partner" in q or "university" in q:
        return PREDEFINED_QA["partners"]

    return None


# -----------------------------
# LOAD DOCUMENTS + BUILD INDEX
# -----------------------------
@st.cache_resource(show_spinner=True)
def load_index_and_docs():
    files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith((".pdf", ".txt", ".docx"))]

    if len(files) == 0:
        return None, []

    docs = SimpleDirectoryReader(DATA_DIR).load_data()

    # Simple retrieval (no embeddings)
    index = VectorStoreIndex.from_documents(docs, embed_model=None)

    return index, docs


index, DOCUMENTS = load_index_and_docs()

if index is None:
    st.error("❌ No documents found in the data/ folder.\n\nPlease add PDF, TXT, or DOCX files and refresh.")
    st.stop()

# -----------------------------
# SIMPLE KEYWORD RETRIEVAL
# -----------------------------
def keyword_retrieval(query):
    if not DOCUMENTS:
        return "❌ No documents found in the data/ folder."

    q = query.lower().strip()
    matches = []

    for d in DOCUMENTS:
        text = d.text.lower()
        if q in text:
            matches.append(d.text[:2000])

    if matches:
        return "\n\n---\n\n".join(matches)

    return "No relevant information found."


class RetrievalOnlyEngine:
    def query(self, q):
        return keyword_retrieval(str(q))


query_engine = RetrievalOnlyEngine()


# -----------------------------
# CLEAN BULLETS
# -----------------------------
def clean_bullets(text):
    bullets = re.findall(r"[•\-]\s*(.+)", text)
    cleaned = []

    for b in bullets:
        if len(b.strip()) > 1 and b not in cleaned:
            cleaned.append(f"- {b.strip()}")

    return "\n".join(cleaned) if cleaned else None


# -----------------------------
# TRAINING PROGRAM EXTRACTION
# -----------------------------
def extract_training_programs():
    if not DOCUMENTS:
        return None

    output = []

    for d in DOCUMENTS:
        text = d.text

        m = re.search(
            r"(Training Offerings|Job-Oriented Career Programs)([\s\S]{0,2000})",
            text,
            re.IGNORECASE,
        )
        if not m:
            continue

        block = m.group(2)
        bullets = clean_bullets(block)
        if bullets:
            for line in bullets.split("\n"):
                if line not in output:
                    output.append(line)

    return "\n".join(output) if output else None


# -----------------------------
# FINAL ANSWER CLEANER
# -----------------------------
def extract_clean_answer(raw_text, user_query):
    uq = user_query.lower()

    if any(key in uq for key in [
        "training program", "training programs", "courses offered",
        "what courses", "training offerings", "job oriented career"
    ]):
        extracted = extract_training_programs()
        if extracted:
            return extracted

    bullets = clean_bullets(raw_text)
    if bullets:
        return bullets

    return raw_text.strip()[:3000]


# -----------------------------
# UI
# -----------------------------
st.title("🤖 Rooman Knowledge Assistant")

user_query = st.text_input("Ask the Rooman Knowledge Assistant:")

if user_query:
    faq = check_predefined_answers(user_query)

    if faq:
        answer = faq
    else:
        with st.spinner("Searching your documents..."):
            raw = query_engine.query(user_query)
        answer = extract_clean_answer(str(raw), user_query)

    st.subheader("Answer:")
    st.markdown(answer)
