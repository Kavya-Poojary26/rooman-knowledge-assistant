🌟 **Rooman Knowledge Assistant**  
**An Intelligent PDF-Powered Question-Answer Agent Built with Streamlit & LlamaIndex**

---

📘 **Overview**  
Rooman Knowledge Assistant is a lightweight, fast, and reliable AI agent designed to answer user queries using:

- **Organization knowledge (PDF documents)**
- **Keyword-based retrieval**

This tool helps with internal knowledge lookup, training support, FAQ automation, and quick information discovery — all **without cloud LLMs**, ensuring speed, privacy, and zero operational cost.

---

🚀 **Features**

✅ **Dynamic PDF Knowledge Search**  
Extracts and retrieves relevant text from PDFs placed inside the `data/` folder.

✅ **Predefined Q&A Engine**  
Fast retrieval for common or repeated questions using a dictionary-based lookup.

✅ **Smart Keyword Matching**  
Understands important words in queries and returns the closest appropriate answer.

✅ **Lightweight Streamlit UI**  
Clean, fast, and easy to deploy.

✅ **Fully Deployable on Streamlit Cloud**  
Just push to GitHub → Deploy → Use.

---

🧰 **Tech Stack & Tools Used**

🖥️ **Frontend**
- Streamlit (UI & interaction)

🧠 **AI & Retrieval**
- LlamaIndex – PDF loading, parsing, and extraction  
- Keyword-Matching Engine  
- Predefined Answer Engine  

🗂️ **Storage**
- Local `data/` folder for PDFs  
- No external database needed  

🔧 **Languages & Frameworks**
- Python 3.10  
- Streamlit  
- LlamaIndex  

---

⚙️ **Setup & Run Instructions**

**1️⃣ Clone the Repository**
git clone https://github.com/Kavya-Poojary26/rooman-knowledge-assistant
cd rooman-knowledge-assistant

markdown
Copy code

**2️⃣ Install Dependencies**
pip install -r requirements.txt

markdown
Copy code

**3️⃣ Add Your PDF Documents**  
Place all your PDFs inside the `data/` directory:
data/
rooman_technologies.pdf

markdown
Copy code

**4️⃣ Run the App**
streamlit run app.py

yaml
Copy code

**5️⃣ Deploy on Streamlit Cloud**
- Visit: https://share.streamlit.io  
- Connect your GitHub repo  
- Select **main → app.py**  
- Deploy 🎉  

---

🚧 **Potential Improvements**
- Add embeddings + vector search (Chroma / FAISS)  
- Add OpenAI / Gemini reasoning layer  
- Multi-PDF support  
- Better keyword extraction (spaCy / NLTK)  
- Chat history & memory  
- Admin panel for dynamic Q&A updates  
- Voice input + TTS  

---

🏁 **Conclusion**  
Rooman Knowledge Assistant is a fast, practical, and privacy-friendly knowledge engine perfect for organ
