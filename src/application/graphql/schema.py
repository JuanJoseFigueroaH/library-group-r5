import strawberry
from typing import Any, Optional

@strawberry.type
class BookType:
    id: int
    title: str
    subtitle: str
    author: str
    category: str
    datetime_publication: str
    editor: str
    description: str


@strawberry.type
class BaseResponseDTO:
    api_version: str
    method: str
    data: Optional[BookType]