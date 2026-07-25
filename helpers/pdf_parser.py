import io
import fitz  # PyMuPDF
import pdfplumber

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from a PDF file using PyMuPDF (fitz) for speed,
    falling back to pdfplumber if PyMuPDF fails or extracts empty text.
    
    Args:
        pdf_file: File path, bytes, or Streamlit UploadedFile object.
        
    Returns:
        str: Extracted text cleaned of excessive whitespace.
    """
    text = ""
    pdf_bytes = None

    # Obtain raw bytes if pdf_file is a Streamlit UploadedFile or file-like object
    if hasattr(pdf_file, "getvalue"):
        pdf_bytes = pdf_file.getvalue()
    elif hasattr(pdf_file, "read"):
        pdf_bytes = pdf_file.read()
        if hasattr(pdf_file, "seek"):
            pdf_file.seek(0)
    elif isinstance(pdf_file, bytes):
        pdf_bytes = pdf_file
    elif isinstance(pdf_file, str):
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()

    # Try fast extraction with PyMuPDF (fitz)
    if pdf_bytes:
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                page_text = page.get_text("text")
                if page_text:
                    text += page_text + "\n"
            doc.close()
        except Exception as e:
            text = ""

    # Fallback to pdfplumber if text is still empty
    if not text.strip() and pdf_bytes:
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            pass

    return text.strip()
