# app.py
import streamlit as st
import os

# Set page configuration
st.set_page_config(page_title="LegalLens AI", layout="wide")

# Retrieve API keys from st.secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    serpapi_key = st.secrets["SERPAPI_KEY"]
except KeyError as e:
    st.error("API keys are not set in your secrets. Please add GEMINI_API_KEY and SERPAPI_KEY to your .streamlit/secrets.toml file or set them in your Streamlit Cloud dashboard.")
    st.stop()

# Import functions from backend and initialize the model using the provided API key
from backend.document_parser import extract_text_from_file
from backend.llm_processor import (
    load_model,
    summarize_contract,
    answer_question,
    generate_what_if_scenarios,
    generate_red_flags,
    generate_clause_breakdown
)
from backend.rag_pipeline import get_combined_context
from utils.helpers import clean_llm_markdown

# Load the model with the API key
model = load_model(api_key)

# Custom styling for the app
st.markdown("""
    <style>
    /* General font and smoothing */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    /* Hide Streamlit header/footer */
    #MainMenu, footer {visibility: hidden;}
    /* Card-style shadows for buttons and inputs */
    .stButton > button {
        border-radius: 10px;
        background-color: #00ADB5;
        color: white;
        padding: 0.6rem 1.4rem;
        font-weight: 500;
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #00cfd1;
        color: #121212;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    /* Input fields */
    .stTextInput > div > input,
    .stTextArea textarea {
        background-color: #fff;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        padding: 0.6rem;
    }
    /* Expander style */
    details summary {
        font-weight: 600;
        background-color: #f7f7f7;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    /* Subheader spacing */
    .stSubheader {
        margin-top: 2rem;
        font-size: 1.4rem;
    }
    /* Section containers (optional) */
    .stMarkdown {
        background-color: #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("LegalLens AI")
st.write("Understand your legal documents in plain English...")

# Initialize session state
if "contract_text" not in st.session_state:
    st.session_state["contract_text"] = ""
if "user_age" not in st.session_state:
    st.session_state["user_age"] = 25
if "user_context" not in st.session_state:
    st.session_state["user_context"] = ""

# Sidebar inputs
age = st.sidebar.number_input("Your Age", min_value=10, max_value=100, value=25)
context = st.sidebar.text_area("Context (optional)", placeholder="e.g., I'm a student signing a lease...", value=st.session_state["user_context"])
if st.sidebar.button("Save Context"):
    st.session_state["user_age"] = age
    st.session_state["user_context"] = context
    st.sidebar.success("Context saved!")

# File uploader for contracts
uploaded_file = st.file_uploader("Upload your contract (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Extracting text from document..."):
        raw_text = extract_text_from_file(uploaded_file)
        st.session_state["contract_text"] = raw_text
        # Update session state with the latest age and context when a file is uploaded
        st.session_state["user_age"] = age
        st.session_state["user_context"] = context

    if raw_text:
        st.subheader("Document Extracted")

        # Helper function to generate a concise query from the document text
        def generate_document_query(raw_text, task, max_length=50):
            # Take the first few words of the document as a base query
            words = raw_text.split()[:10]
            base_query = " ".join(words)
            # Add task-specific context
            if task == "summarize":
                return f"summarize legal document {base_query}"
            elif task == "what_if":
                return f"what if scenarios for legal contract {base_query}"
            elif task == "red_flags":
                return f"red flags in legal contract {base_query}"
            elif task == "clause_breakdown":
                return f"clause breakdown of legal contract {base_query}"
            return base_query

        if st.button("Summarize This Document"):
            with st.spinner("Summarizing..."):
                # Generate a targeted query for summarization
                search_query = generate_document_query(raw_text, "summarize")
                if context:
                    search_query += f" {context}"
                combined_context = get_combined_context(search_query)
                summary = summarize_contract(model, raw_text, age=age, context=context + "\n\n" + combined_context)
                st.success("Summary Ready")
                st.markdown(clean_llm_markdown(summary))
                with st.expander("View Context"):
                    st.write(combined_context)

        if st.button("What If Simulator"):
            with st.spinner("Simulating scenarios..."):
                # Generate a targeted query for what-if scenarios
                search_query = generate_document_query(raw_text, "what_if")
                if context:
                    search_query += f" {context}"
                combined_context = get_combined_context(search_query)
                what_if = generate_what_if_scenarios(model, raw_text, age=age, context=context + "\n\n" + combined_context)
                st.subheader("What If Scenarios")
                st.markdown(clean_llm_markdown(what_if))
                with st.expander("View Context"):
                    st.write(combined_context)

        if st.button("Red Flag Radar"):
            with st.spinner("Scanning..."):
                # Generate a targeted query for red flags
                search_query = generate_document_query(raw_text, "red_flags")
                if context:
                    search_query += f" {context}"
                combined_context = get_combined_context(search_query)
                red_flags = generate_red_flags(model, raw_text, age=age, context=context + "\n\n" + combined_context)
                st.subheader("Red Flag Radar")
                st.markdown(clean_llm_markdown(red_flags))
                with st.expander("View Context"):
                    st.write(combined_context)

        if st.button("Clause-by-Clause Breakdown"):
            with st.spinner("Breaking down..."):
                # Generate a targeted query for clause breakdown
                search_query = generate_document_query(raw_text, "clause_breakdown")
                if context:
                    search_query += f" {context}"
                combined_context = get_combined_context(search_query)
                breakdown = generate_clause_breakdown(model, raw_text, age=age, context=context + "\n\n" + combined_context)
                st.subheader("Clause-by-Clause Breakdown")
                st.markdown(clean_llm_markdown(breakdown))
                with st.expander("View Context"):
                    st.write(combined_context)

        st.subheader("Still Confused? Ask Me Anything")
        user_question = st.text_input("Ask a legal question...")
        if user_question:
            with st.spinner("Thinking..."):
                # Enhance the user question with context for better search
                search_query = user_question
                if context:
                    search_query += f" {context}"
                search_query += " in legal contracts"
                combined_context = get_combined_context(search_query)
                answer = answer_question(model, user_question, raw_text, age=age, context=context + "\n\n" + combined_context)
                st.info(answer)
                with st.expander("View Context"):
                    st.write(combined_context)
else:
    st.info("Please upload a contract to begin.")