# Boss Wallah – Course Support Chatbot 

This project is a **Retrieval-Augmented Generation (RAG) chatbot** built using Streamlit that can answer questions about Boss Wallah courses and provide local information via Google Maps. It supports **multi-language queries** and has special rules for certain topics (e.g., dairy farm queries).

---

## **Features**

- Query Boss Wallah course dataset and retrieve answers.
- Multi-language support: Hindi, Kannada, Tamil, Telugu, Malayalam.
- Special handling for dairy farm queries (numbers extracted automatically).
- Integration with Google Maps API for local information like stores, restaurants, etc.
- Fast retrieval using FAISS vector index and SentenceTransformer embeddings.

---

## **Project Structure**
## Installation

1. Clone the Repository
   ``` sh
   git clone https://github.com/Jintuvc/rag_chatbot.git
   cd rag
   ```
2. Create a Virtual Environment
   ```
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ````
3. Install Dependencies
   ```
   pip install -r requirements.txt
   ```
4. Set Geocoding API Key
   ```
   API_KEY=your_api_key
   ```
5. Run the App
   ```
   streamlit run app.py
   ```

## How It Works
- 

## Tech Stack
- Python
- LangChain + OpenAI (GPT-3.5)
- FAISS (Vector Search)
- Streamlit (UI)
- PyMuPDF, python-docx, python-pptx, pandas (for document parsing)


