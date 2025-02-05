import logging
import chromadb
import uuid

logger = logging.getLogger(__name__)


class PdfReaderStorge():
    client = chromadb.PersistentClient("./mycollection")

    def create_collection(collection_name, client):
        """Create or retrieve a collection in the database."""
        try:
            collection = client.get_or_create_collection(
                name=collection_name, metadata={"hnsw:space": "cosine"})
            return collection
        except Exception as ex:
            logger.error(f"Error in creating a collection: {ex}")

    def add_to_collection(text_chunks, collection):
        """Add text chunks to the collection with unique ids."""
        try:
            documents = []
            ids = []

            for idx, text in enumerate(text_chunks):
                random_id = str(uuid.uuid4())
                ids.append(f"chunk_id{idx}_unique_id_{random_id}")
                documents.append(text)

            collection.add(
                documents=documents,
                ids=ids
            )
            print(f"Added {len(documents)} chunks to the collection.")
        except Exception as ex:
            logger.error(f"Error to add in collection: {ex}")
