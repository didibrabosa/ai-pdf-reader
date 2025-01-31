import logging
import chromadb
import getpass
import uuid
import os
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from PyPDF2 import PdfReader
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass(
        "Enter API key for OpenAI: ")

app = FastAPI()

chat_model = ChatOpenAI(
    model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

client = chromadb.PersistentClient("./mycollection")


def read_pdf(file):
    return PdfReader(file)


def extract_text_from_pdf(reader):
    try:
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
        return text
    except Exception as ex:
        logger.error(f"Error in extract text form pdf: {ex}")


def create_collection(collection_name, client):
    try:
        collection = client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"})
        return collection
    except Exception as ex:
        logger.error(f"Error in creating a collection: {ex}")


def add_to_collection(text_chunks, collection):
    try:
        documents = []
        ids = []

        for idx, text in enumerate(text_chunks):
            random_id = str(uuid.uuid4())
            ids.append(f"chunk_id{idx}_unique_id_{random_id}")
            documents.append(text.pages_content)

        collection.add(
            documents=documents,
            ids=ids
        )
    except Exception as ex:
        logger.error(f"Error to add in collection: {ex}")
