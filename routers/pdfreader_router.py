import logging
from fastapi import APIRouter, HTTPException
from models.pdfreader_model import PdfReaderModel
from services.pdfreader_service import PdfReaderService
from storages.pdfreader_storage import PdfReaderStorage

router = APIRouter()

logger = logging.getLogger(__name__)

service = PdfReaderService(storage=PdfReaderStorage())


@router.post("/ask_ai")
async def ask_to_ai(request: PdfReaderModel):
    """Process a question and return an AI-generated answer."""
    try:
        logger.info("Starting question to AI...")

        relevant_text = service.get_relevant_text(request.question)

        if not relevant_text:
            raise HTTPException(
                status_code=404, detail="No relevant document found.")

        response = service.invoke_ai(relevant_text.context, request.question)

        return {"answer": response.content}

    except Exception as ex:
        logger.error(f"Error while asking question: {ex}")
        raise HTTPException(
            status_code=500, detail="Internal Server Error")
