import logging
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class PdfReaderProcessor:
    pdf_path = "Harry_Potter_AI.pdf"

    def read_pdf(file):
        """Read a PDF file and return its reader object."""
        result = PdfReader(file)
        return result

    def extract_text_from_pdf(reader):
        """Extract and return text from each page of the PDF reader."""
        try:
            text = ""
            for page_num, page in enumerate(reader.pages):
                extract_text = page.extract_text()
                if extract_text:
                    text += extract_text + "\n\n"
                else:
                    logger.warning(f"Text not found {page_num}")

            return text
        except Exception as ex:
            logger.error(f"Error in extract text form pdf: {ex}")

    def split_text_from_pdf(text, chunk_size=1000, chunk_overlap=200):
        """Split text into chunks with given size and overlap."""
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    ". ", "... ", ", ", "! ", "? ", "\n\n", "\n", " ", ""],
            )

            return text_splitter.split_text(text)
        except Exception as ex:
            logger.error(f"Error in splitter a document: {ex}")
