import logging
from PyPDF2 import PdfReader


class PdfReaderService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pdf = "Harry_Potter_AI.pdf"

    def read_pdf(self):
        """Read a PDF file and return its reader object."""
        self.logger.info("Starting to read the PDF...")

        result = PdfReader(self.pdf)
        return result

    def extract_text_from_pdf(self, reader):
        """Extract and return text from each page of the PDF reader."""
        try:
            self.logger.info("Starting to extract the text from PDF...")

            text = ""
            for page_num, page in enumerate(reader.pages):
                extract_text = page.extract_text()

                if extract_text:
                    text += extract_text + "\n\n"
                else:
                    self.logger.warning(f"Text not found {page_num}")

            return text

        except Exception as ex:
            self.logger.error(f"Error in extract text form pdf: {ex}")
            raise
