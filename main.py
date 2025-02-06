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

    #Alguns pontos aqui: 
    # - Essa classe (PdfReaderStorge) nunca é instanciada, e vc esta chamando seus métodos como se fossem métodos estáticos.
    # - Pq vc ta passando a instancia do client da mesma classe pro método create_collection? Se ele ja tem a referencia pro objeto dentro da classe
    collection = PdfReaderStorge.create_collection(
        "pdf_collection", client=PdfReaderStorge.client
    )

    # Mesma coisa aqui, por que passar a variavel pdf_path se vc ja tem ela dentro da mesma classe? 
    reader = PdfReaderProcessor.read_pdf(
        PdfReaderProcessor.pdf_path)

    text = PdfReaderProcessor.extract_text_from_pdf(reader)
    text_chunks = PdfReaderProcessor.split_text_from_pdf(text)

    PdfReaderStorge.add_to_collection(text_chunks, collection)

    #Pq vc ta adicionando esse objeto ao router? 
    PdfReaderRouter.collection = collection

    yield

    logger.info("Shutdown application...")
    PdfReaderStorge.client.delete_collection("pdf_collection")
    logger.info("Database cleaned up!")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
