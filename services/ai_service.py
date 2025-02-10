import os
import logging
from langchain_openai import ChatOpenAI
from models.rag_model import AIResponse


class AIService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.chat_model = ChatOpenAI(
            model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"]
        )

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
