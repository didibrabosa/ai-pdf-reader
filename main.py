import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.pdfreader_router import PdfReaderRouter, router
from storages.pdfreader_storage import PdfReaderStorge
from documents.pdfreader_processor import PdfReaderProcessor

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    "Lifecycle menagement for the application."
    logger.info("Starting the application...")

    collection = PdfReaderStorge.create_collection(
        "pdf_collection", client=PdfReaderStorge.client
    )

    reader = PdfReaderProcessor.read_pdf(
        PdfReaderProcessor.pdf_path)

    text = PdfReaderProcessor.extract_text_from_pdf(reader)
    text_chunks = PdfReaderProcessor.split_text_from_pdf(text)

    PdfReaderStorge.add_to_collection(text_chunks, collection)
    PdfReaderRouter.collection = collection

    yield

    logger.info("Shutdown application...")
    PdfReaderStorge.client.delete_collection("pdf_collection")
    logger.info("Database cleaned up!")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
