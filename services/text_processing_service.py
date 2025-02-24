import logging
from models.rag_model import RelevantText, AIResponse
from storages.text_storage import TextStorage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.ai_service import AIService


class TextProcessingService:
    def __init__(self, storage: TextStorage, ai_service: AIService):
        self.logger = logging.getLogger(__name__)
        self.storage = storage
        self.ai_service = ai_service

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

            relevant_texts = [doc for doc in results.documents[0]]
            context = " ".join(relevant_texts)

            return RelevantText(texts=relevant_texts, context=context)

        except Exception as ex:
            self.logger.error(
                f"Error in catching the most relevant texts: {ex}")

    def invoke_ai(self, context, question) -> AIResponse:
        """Invoke AI with the given context and question."""
        return self.ai_service.invoke_ai(context, question)
