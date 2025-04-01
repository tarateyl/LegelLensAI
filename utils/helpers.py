from gtts import gTTS
import os
import re

def generate_audio(text, filename="podcast_summary.mp3"):
    try:
        tts = gTTS(text=text, lang='en')
        filepath = f"./{filename}"
        tts.save(filepath)
        return filepath
    except Exception as e:
        print(f"❌ Audio generation error: {e}")
        return None

def clean_llm_markdown(text):
    # Add space between asterisks and words (if missing)
    text = re.sub(r'\*(\S)', r'* \1', text)  # *word → * word
    text = re.sub(r'(\S)\*', r'\1 *', text)  # word* → word *

    # Fix aggressively squished italic phrases
    text = re.sub(r'\*([a-zA-Z0-9]{10,})\*', r'\1', text)  # remove * from loooong tokens

    # Handle common Gemini mistakes: unclosed or nested asterisks
    text = re.sub(r'(\*+)\s+', r'\1 ', text)  # ensure space after stars
    text = re.sub(r'\s+(\*+)', r' \1', text)  # ensure space before stars

    # Normalize triple asterisks
    text = text.replace("***", "**")

    # Remove stray italic phrases that break layout
    text = re.sub(r'\*(\w{5,})\*', r'\1', text)

    return text.strip()