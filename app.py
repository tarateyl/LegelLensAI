import streamlit as st
import os
<<<<<<< HEAD
=======


st.set_page_config(page_title="LegalLens AI", layout="wide")


>>>>>>> 2036bb5 (first commit)
from backend.document_parser import extract_text_from_file
from backend.llm_processor import (
    summarize_contract,
    answer_question,
    generate_what_if_scenarios,
    generate_red_flags,
    generate_clause_breakdown
)
from backend.rag_pipeline import get_glossary_context
from utils.helpers import generate_audio, clean_llm_markdown

# --- Streamlit App --- #
st.set_page_config(page_title="LegalLens AI", layout="wide")

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

# Session state setup
if "contract_text" not in st.session_state:
    st.session_state["contract_text"] = ""
if "user_age" not in st.session_state:
    st.session_state["user_age"] = 25
if "user_context" not in st.session_state:
    st.session_state["user_context"] = ""

# Sidebar input
age = st.sidebar.number_input("Your Age", min_value=10, max_value=100, value=25)
context = st.sidebar.text_area("Context (optional)", placeholder="e.g., I'm a student...")

uploaded_file = st.file_uploader("Upload your contract (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Extracting text from document..."):
        raw_text = extract_text_from_file(uploaded_file)
        st.session_state["contract_text"] = raw_text
        st.session_state["user_age"] = age
        st.session_state["user_context"] = context

    if raw_text:
        st.subheader("Document Extracted")

        if st.button("Summarize This Document"):
            with st.spinner("Summarizing..."):
                glossary = get_glossary_context(raw_text)
                summary = summarize_contract(model, raw_text + "\n\n" + glossary, age=age, context=context)
                st.success("Summary Ready")
                st.markdown(clean_llm_markdown(summary))

        if st.button("What If Simulator"):
            with st.spinner("Simulating scenarios..."):
                what_if = generate_what_if_scenarios(model, raw_text, age=age, context=context)
                st.subheader("What If Scenarios")
                st.markdown(clean_llm_markdown(what_if))

        if st.button("Red Flag Radar"):
            with st.spinner("Scanning..."):
                red_flags = generate_red_flags(model, raw_text, age=age, context=context)
                st.subheader("Red Flag Radar")
                st.markdown(clean_llm_markdown(red_flags))

        if st.button("Clause-by-Clause Breakdown"):
            with st.spinner("Breaking down..."):
                breakdown = generate_clause_breakdown(model, raw_text, age=age, context=context)
                st.subheader("Clause-by-Clause Breakdown")
                st.markdown(clean_llm_markdown(breakdown))

        st.subheader("Still Confused? Ask Me Anything")
        user_question = st.text_input("Ask a legal question...")
        if user_question:
            with st.spinner("Thinking..."):
                glossary = get_glossary_context(user_question)
                answer = answer_question(model, user_question + "\n\n" + glossary, raw_text, age=age, context=context)
                st.info(answer)
else:
    st.info("Please upload a contract to begin.")
