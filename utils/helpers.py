from gtts import gTTS
import os
import re

def clean_llm_markdown(text):

    """
    Clean the LLM output by removing unwanted markdown formatting.
    This function removes extra asterisks, underscores, and extra spaces.
    """
    # Remove asterisks (commonly used for bullet points or emphasis)
    cleaned = re.sub(r'\*+', '', text)
    # Remove underscores (used for emphasis in Markdown)
    cleaned = re.sub(r'_+', '', cleaned)
    # Optionally, remove other markdown characters if needed:
    # For example, backticks (often used for code formatting)
    cleaned = re.sub(r'`+', '', cleaned)
    # Replace multiple newlines with a maximum of two newlines
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    return cleaned.strip()

    # # Add space between asterisks and words (if missing)
    # text = re.sub(r'\*(\S)', r'* \1', text)  # *word → * word
    # text = re.sub(r'(\S)\*', r'\1 *', text)  # word* → word *

    # # Fix aggressively squished italic phrases
    # text = re.sub(r'\*([a-zA-Z0-9]{10,})\*', r'\1', text)  # remove * from loooong tokens

    # # Handle common Gemini mistakes: unclosed or nested asterisks
    # text = re.sub(r'(\*+)\s+', r'\1 ', text)  # ensure space after stars
    # text = re.sub(r'\s+(\*+)', r' \1', text)  # ensure space before stars

    # # Normalize triple asterisks
    # text = text.replace("***", "**")

    # # Remove stray italic phrases that break layout
    # text = re.sub(r'\*(\w{5,})\*', r'\1', text)

    # return text.strip()
   