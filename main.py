import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.pdfreader_router import router
from storages.pdfreader_storage import PdfReaderStorage
from services.pdfreader_service import PdfReaderService
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    "Lifecycle menagement for the application."
    logger.info("Starting the application...")

    pdf_storage = PdfReaderStorage()
    pdf_service = PdfReaderService(storage=pdf_storage)

    reader = pdf_service.read_pdf()
    text = pdf_service.extract_text_from_pdf(reader)
    text_chunks = pdf_service.split_text_from_pdf(text)

    pdf_storage.add_to_collection(text_chunks)

    yield

    logger.info("Shutdown application...")
    pdf_storage.client.delete_collection("pdf_collection")
    logger.info("Database cleaned up!")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
