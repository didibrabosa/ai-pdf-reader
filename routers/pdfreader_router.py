import logging
from fastapi import APIRouter, HTTPException
from models.pdfreader_model import PdfReaderModel
from langchain_openai import ChatOpenAI
from services.pdfreader_service import PdfReaderService
from storages.pdfreader_storage import PdfReaderStorage
import os

router = APIRouter()

logger = logging.getLogger(__name__)

chat_model = ChatOpenAI(
    model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

service = PdfReaderService(storage=PdfReaderStorage())


@router.post("/ask_ai")
async def ask_to_ai(request: PdfReaderModel):
    """Process a question and return an AI-generated answer."""
    try:
        logger.info("Starting question to AI...")

        context = service.get_relevant_text(request.question)

        if not context:
            raise HTTPException(
                status_code=404, detail="None document relevent fouded.")

        response = chat_model.invoke(context + request.question)

        return {"answer": response.content}

    except Exception as ex:
        logger.error(f"Error while asking question: {ex}")
        raise HTTPException(
            status_code=500, detail="Internal Server Error")
