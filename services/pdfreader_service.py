import os
import logging
from models.pdfreader_model import RelevantText, AIResponse
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from storages.pdfreader_storage import PdfReaderStorage
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PdfReaderService:
    def __init__(self, storage: PdfReaderStorage):
        self.logger = logging.getLogger(__name__)
        self.pdf = "Harry_Potter_AI.pdf"
        self.storage = storage
        self.chat_model = ChatOpenAI(
            model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

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

    def split_text_from_pdf(self, text, chunk_size=1000, chunk_overlap=200):
        """Split text into chunks with given size and overlap."""
        try:
            self.logger.info("Starting to split text from PDF...")

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    ". ", "... ", ", ", "! ", "? ", "\n\n", "\n", " ", ""],
            )

            return text_splitter.split_text(text)

        except Exception as ex:
            self.logger.error(f"Error in splitter a document: {ex}")

    def get_relevant_text(self, question) -> RelevantText:
        """Get the most relevant texts for the question and ivoke AI."""
        try:
            self.logger.info("Catching the most relevant texts...")

            results = self.storage.query_collection(query_text=question)

            if not results or not results.documents:
                return RelevantText(texts=[], context="")

            relevant_texts = [doc[0] for doc in results.documents]
            context = " ".join(relevant_texts)

            return RelevantText(texts=relevant_texts, context=context)

        except Exception as ex:
            self.logger.error(
                f"Error in catching the most relevant texts: {ex}")

    def invoke_ai(self, context, question) -> AIResponse:
        """Invoke AI with the given context and question."""
        try:
            self.logger.info("Invoke AI...")

            if not context:
                return None

            response = self.chat_model(context + question)
            return AIResponse(content=response.content)

        except Exception as ex:
            self.logger.error(f"Error in invoking AI: {ex}")
