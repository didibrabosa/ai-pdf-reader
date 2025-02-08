from pydantic import BaseModel
from typing import List


class PdfReaderModel(BaseModel):
    """Data model for a question request."""
    question: str


class QueryResult(BaseModel):
    """Data model for the result of a query to the document collection."""
    documents: List[List[str]]


class AIResponse(BaseModel):
    """Data model for the response generated by the AI."""
    content: str


class RelevantText(BaseModel):
    """Data model for relevant texts and their concatenated context."""
    texts: List[str]
    context: str
