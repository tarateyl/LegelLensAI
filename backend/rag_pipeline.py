import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
import pickle

# Load glossary and build RAG store
def get_glossary_context(query, k=3):
    try:
        glossary_path = "data/legal_glossary.txt"
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
