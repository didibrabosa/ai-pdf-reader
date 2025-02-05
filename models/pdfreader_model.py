from pydantic import BaseModel


class PdfReaderModel(BaseModel):
    """Data model for a question request."""
    question: str
