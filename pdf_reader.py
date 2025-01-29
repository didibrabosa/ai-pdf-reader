from PyPDF2 import PdfReader
import logging


logger = logging.getLogger(__name__)


def read_pdf(file):
    return PdfReader(file)


def extract_text_from_pdf(reader):
    try:
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
        return text
    except Exception as e:
        logger.error(f"Having following issue with extract_text_from_pdf - {e}")
