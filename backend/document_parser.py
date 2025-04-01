import fitz  # PyMuPDF
import tempfile

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.type

    try:
        if file_type == "text/plain":
            return uploaded_file.read().decode("utf-8")

        elif file_type == "application/pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            doc = fitz.open(tmp_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            return text.strip()

        else:
            return None
    except Exception as e:
        print(f"Error extracting file: {e}")
        return None
