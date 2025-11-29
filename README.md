🧠 Rooman Knowledge Assistant
An Intelligent PDF-Powered Question-Answer Agent Built with Streamlit & LlamaIndex
📘 Overview

Rooman Knowledge Assistant is a lightweight, fast, and reliable AI agent designed to answer user queries using:

Organization knowledge (PDF documents)

Predefined question–answer pairs

Smart keyword-based retrieval

This assistant is built for internal knowledge lookup, training support, FAQ automation, and quick information discovery for Rooman Technologies.

It delivers accurate answers without relying on heavy cloud LLMs, ensuring speed, privacy, and cost-efficiency.

🚀 Features
✅ Dynamic PDF Knowledge Search

Extracts relevant answers from uploaded PDFs inside the data/ folder.

✅ Predefined Q&A Engine

Fast retrieval for common questions using structured dictionary-based logic.

✅ Smart Keyword Matching

Detects important keywords from user queries to return the closest answer.

✅ Lightweight Streamlit UI

Clean interface, fast response, zero-complexity deployment.

✅ Fully Deployable on Streamlit Cloud

Just connect GitHub → deploy → use instantly.

⚠️ Limitations

Works best for fact-based queries, not reasoning-heavy questions

Accuracy depends on the quality of PDF text extraction

No conversation memory (stateless responses)

Designed for single-document setups (can be extended)

🧰 Tech Stack & Tools Used
🖥️ Frontend

Streamlit – clean UI for user queries and results

🧠 AI & Retrieval

LlamaIndex (SimpleDirectoryReader) – PDF loading & text extraction

Keyword-Based Retrieval Engine – fast matching

Predefined Answer Engine – instant replies

🗂️ Data Storage

Local data directory (/data) for documents

Local processing, no external DB needed

🔧 Languages & Frameworks

Python 3.10

Streamlit

LlamaIndex

OS / Pathlib utilities

⚙️ Setup & Run Instructions
1️⃣ Clone the Repository
git clone https://github.com/Kavya-Poojary26/rooman-knowledge-assistant
cd rooman-knowledge-assistant

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Add Your PDF Documents

Place all your PDFs inside:

data/


Example:

data/rooman_technologies.pdf

4️⃣ Run the App
streamlit run app.py

5️⃣ Deploy on Streamlit Cloud

Go to: https://share.streamlit.io

Connect your GitHub

Select your repo → main branch → app.py

Deploy 🎉

🚧 Potential Improvements (Future Scope)

Add embeddings + vector search (Chroma / FAISS)

Add OpenAI / Gemini LLM reasoning when needed

Add multi-PDF support and document selection

Improve keyword extraction with spaCy / NLTK

Add chat history + memory

Add admin dashboard to update predefined Q&A dynamically

Add voice input + TTS output

🏁 Conclusion

Rooman Knowledge Assistant is a fast, clean, and practical knowledge engine ideal for handling organizational FAQs and document-based queries.
Built for speed, usability, and reliability — perfect for internal teams and training workflows.
