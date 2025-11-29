import os
import re
from datetime import datetime
from dotenv import load_dotenv

# Load .env (GROQ_API_KEY)
load_dotenv()

# ----------------------------
# PDF READER
# ----------------------------
try:
    from pypdf import PdfReader
except Exception:
    from PyPDF2 import PdfReader

# ----------------------------
# LlamaIndex Imports
# ----------------------------
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.groq import Groq


# ========================================================
# PDF → TEXT EXTRACTION
# ========================================================
def read_pdfs_text(data_dir="data"):
    texts = {}
    for fname in os.listdir(data_dir):
        if not fname.lower().endswith(".pdf"):
            continue

        path = os.path.join(data_dir, fname)
        pages = []

        try:
            reader = PdfReader(path)
            for page in reader.pages:
                try:
                    pages.append(page.extract_text() or "")
                except:
                    pages.append("")
        except Exception:
            pages.append("")

        texts[fname] = "\n".join(pages)

    return texts


# ========================================================
# BUILD QUERY ENGINE (GROQ LLM)
# ========================================================
def build_query_engine():
    print("Building index using Groq LLM...")

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise RuntimeError("❌ GROQ_API_KEY not found in .env")

    # Configure LLM
    Settings.llm = Groq(
        api_key=groq_key,
        model="llama-3.1-70b-versatile"
    )

    # Load documents
    documents = SimpleDirectoryReader("data").load_data()

    # Build vector index
    index = VectorStoreIndex.from_documents(documents)

    # Create query engine
    return index.as_query_engine(similarity_top_k=5)


# ========================================================
# CLEAN BULLETS
# ========================================================
def clean_bullets(text):
    lines = []
    for line in text.splitlines():
        ln = line.strip(" -*•").strip()
        if len(ln) > 1:
            lines.append("- " + ln)
    return "\n".join(lines)


# ========================================================
# ANSWER QUESTIONS USING LLM
# ========================================================
def answer_questions_with_llm(texts, qe):
    all_text = "\n".join(texts.values())
    answers = {}

    # -----------------------------------
    # Helper for consistent querying
    # -----------------------------------
    def ask(q):
        resp = qe.query(q)
        return resp.response if hasattr(resp, "response") else str(resp)

    # 1. What is Rooman?
    q1 = (
        "Summarize 'Rooman Technologies' strictly based on the document. "
        "Do NOT add external knowledge. Keep it short."
    )
    answers["What is Rooman Technologies?"] = ask(q1)

    # 2. Programs offered
    q2 = (
        "List all training programs offered by Rooman Technologies mentioned in the document. "
        "One bullet per line."
    )
    answers["What types of training programs does Rooman Technologies offer?"] = clean_bullets(ask(q2))

    # 3. Training features
    q3 = (
        "Extract key features of Rooman Technologies’ training approach. Bullet points only."
    )
    answers["What are the key features of Rooman’s training approach?"] = ask(q3)

    # 4. Experience (years)
    m = re.search(r"Founded in\s*(\d{4})", all_text, re.IGNORECASE)
    if m:
        year = int(m.group(1))
        years = datetime.now().year - year
        answers["How many years of experience does Rooman have?"] = (
            f"Founded in {year} — {years} years of experience."
        )
    else:
        answers["How many years of experience does Rooman have?"] = "Founding year not found."

    # 5. Differentiators
    q5 = (
        "What differentiates Rooman Technologies from other institutes? "
        "List bullet points only based on the document."
    )
    answers["What makes Rooman Technologies different?"] = ask(q5)

    # 6. Branches
    q6 = (
        "Extract all cities, branches, and locations of Rooman Technologies mentioned in the document. "
        "One per line."
    )
    answers["Provide all locations/branches listed in the document."] = ask(q6)

    # 7. Partner organizations
    q7 = (
        "List all partner organizations mentioned in the document. "
        "One bullet per line."
    )
    answers["List all partner organizations mentioned in the document."] =
        clean_bullets(ask(q7))

    return answers


# ========================================================
# MAIN
# ========================================================
def main():
    texts = read_pdfs_text("data")

    if not texts:
        print("❌ No PDFs found inside data/")
        return

    qe = build_query_engine()

    print("\nExtracting answers...\n")
    answers = answer_questions_with_llm(texts, qe)

    for q, a in answers.items():
        print("\n=================================")
        print("Q:", q)
        print("=================================")
        print(a)

    print("\n✔ Completed successfully.\n")


if __name__ == "__main__":
    main()
