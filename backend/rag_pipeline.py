# backend/rag_pipeline.py
import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
import serpapi  # Updated import

# Load glossary and build RAG store
def get_glossary_context(query, k=3):
    try:
        glossary_path = os.path.join(os.path.dirname(__file__), "data/legal_glossary.txt")
        with open(glossary_path, "r") as f:
            glossary_text = f.read()

        # Prepare vector store (cached)
        splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        docs = splitter.split_documents([Document(page_content=glossary_text)])

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.from_documents(docs, embeddings)
        matches = db.similarity_search(query, k=k)

        return "\n\n".join([doc.page_content for doc in matches])
    except Exception as e:
        return f"⚠️ Could not retrieve glossary info: {e}"

# Fetch top 10 Google search results
def get_google_search_context(query, num_results=10):
    try:
        params = {
            "q": query,
            "api_key": os.getenv("SERPAPI_KEY") or st.secrets["SERPAPI_KEY"],
            "num": num_results,
            "location": "United States",
            "hl": "en"
        }
        # Updated to use serpapi.search
        search = serpapi.search(**params)
        results = search.get("organic_results", [])
        
        search_context = []
        for result in results[:num_results]:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            search_context.append(f"{title}: {snippet}")
        
        return "\n\n".join(search_context) if search_context else "No search results found."
    except Exception as e:
        return f"⚠️ Could not retrieve Google search info: {e}"

# Combine glossary and Google search context
def get_combined_context(query, k=3):
    glossary_context = get_glossary_context(query, k)
    google_context = get_google_search_context(query)
    print(f"Glossary Context:\n{glossary_context}\n\nGoogle Search Context:\n{google_context}")
    return f"Glossary Context:\n{glossary_context}\n\nGoogle Search Context:\n{google_context}"