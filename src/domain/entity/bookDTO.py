from typing import List, Optional
from .book import BookEntity
from .source import SourceEntity
from pydantic import BaseModel

class BookDTOEntity(BaseModel):
    books: List[BookEntity]
    source: Optional[SourceEntity]
