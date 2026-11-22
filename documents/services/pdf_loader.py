from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_pdf(file_path: str) -> list[Document]:
    """Loads PDF documents and extract their content.
    Args:
        """
    loader = PyPDFLoader(file_path)

    try:
        pages = loader.load()
        print(f"PDF has {len(pages)} pages")
    except Exception as e:
        print(f"Error : {e}")
        raise

    return pages
