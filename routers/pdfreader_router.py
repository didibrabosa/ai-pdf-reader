import logging
from fastapi import APIRouter, HTTPException
from models.pdfreader_model import PdfReaderModel
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import getpass

router = APIRouter()

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass(
        "Enter API key for OpenAI: ")

logger = logging.getLogger(__name__)

chat_model = ChatOpenAI(
    model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])


class PdfReaderRouter():
    collection = None

    @router.post("/ask_ai")
    async def ask_to_ai(request: PdfReaderModel):
        """Process a question and return an AI-generated answer."""
        try:
            question = request.question

            results = PdfReaderRouter.collection.query(
                query_texts=[question],
                n_results=3
            )
            print(results)

            relevant_texts = [
                result[0] for result in results['documents']]

            context = " ".join(relevant_texts)

            response = chat_model(context + question)

            return {"answer": response.content}

        except Exception as ex:
            logger.error(f"Error while asking question: {ex}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")
