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
4. Add your Google Maps API key in map.py:
   ```
   API_KEY=your_api_key
   ```
5. Run the App
   ```
   streamlit run app.py
   ```

## How It Works
1.Language Detection: Detects query language (Hindi, Kannada, Tamil, Telugu, Malayalam).

2.Dataset Retrieval: Uses FAISS + SentenceTransformer embeddings to retrieve top-k relevant courses.

3.Answer Generation: Converts retrieved data into readable answers.

4.Translation: Translates answers into the user’s query language.

5.Maps Queries: Detects if the query is about stores/places and fetches results from Google Maps API.


## Tech Stack
1.Python 

2.Streamlit – for building the web app interface

3.pandas  – data handling

4.FAISS – fast vector-based retrieval

5.SentenceTransformers – embeddings for semantic search

6.deep-translator – for multi-language translation

7.requests – Google Maps API integration


