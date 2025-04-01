import os
import google.generativeai as genai

import streamlit as st


# Initialize Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-1.5-flash-latest")

model = load_model()

# Summarize Contract with Age + Context
def summarize_contract(text, age=25, context=""):
    prompt = f"""
You are a helpful legal assistant. Explain the following legal document in plain English to a {age}-year-old.
Context: {context}

- Provide a summary
- Highlight obligations or risks
- List unusual clauses or red flags
- Offer practical tips

Legal Document:
{text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f" Error during summarization: {e}"

def answer_question(model, question, text, age=25, context=""):
    prompt = f"""
User is {age}, context: "{context}"

Legal Document:
{text}

User Question:
{question}

Return:
1. Formal summary
2. Friendly podcast-style explanation
(No markdown formatting)
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error answering: {e}"

def generate_what_if_scenarios(model, text, age=25, context=""):
    prompt = f"""
User is {age}, context: "{context}"

Generate 3 real-life "what if" scenarios based on this contract:
{text}
(No markdown formatting)
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating scenarios: {e}"

def generate_red_flags(model, text, age=25, context=""):
    prompt = f"""
Scan this contract for unusual, one-sided, or risky clauses. Context: {context}, Age: {age}
{text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating red flags: {e}"

def generate_clause_breakdown(model, text, age=25, context=""):
    prompt = f"""
Split this contract into clear sections with titles and explanations for a {age}-year-old.
Context: {context}
{text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating breakdown: {e}"
