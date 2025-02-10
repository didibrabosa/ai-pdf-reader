import logging
import chromadb
import uuid
from models.rag_model import QueryResult


class TextStorage():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = chromadb.PersistentClient("./mycollection")
        self.collection = self.client.get_or_create_collection(
            name="pdf_collection",
            metadata={"hnsw:space": "cosine"}
        )

    def add_to_collection(self, text_chunks):
        """Add text chunks to the collection with unique ids."""
        try:
            self.logger.info("Starting to add to the collection...")

            documents = []
            ids = []

            for idx, text in enumerate(text_chunks):
                random_id = str(uuid.uuid4())
                ids.append(f"chunk_id{idx}_unique_id_{random_id}")
                documents.append(text)

            self.collection.add(
                documents=documents,
                ids=ids
            )

            self.logger.info(
                f"Added {len(documents)} chunks to the collection.")

        except Exception as ex:
            self.logger.error(f"Error to add in collection: {ex}")

    def query_collection(self, query_text) -> QueryResult:
        """Query the document collection for texts relevant to the query."""
        try:
            self.logger.info("Starting to querying the collection...")

            results = self.collection.query(
                query_texts=[query_text],
                n_results=3
            )
            return QueryResult(documents=results["documents"])

        except Exception as ex:
            self.logger.error(f"Error to querying the collection: {ex}")
