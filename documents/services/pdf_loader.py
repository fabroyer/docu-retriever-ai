from pypdf import PdfReader

def extrac_text(file_path: str) -> str:
    """Extract text from a PDF file.
    Args:
        """
    reader = PdfReader(file_path)
    extracted_pages = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        extracted_pages.append(page_text)

    full_text = "".join(extracted_pages).strip()

    if not full_text:
        raise ValueError("No text extracted from PDF file.")

    return full_text
