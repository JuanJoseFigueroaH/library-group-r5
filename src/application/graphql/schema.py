import strawberry
from typing import Any, Optional, List, Set

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
class BookTypeEntity:
    id: Optional[str]
    title: Optional[str]
    subtitle: Optional[str]
    authors: Optional[List[str]]
    categories: Optional[List[str]]
    datetime_publication: Optional[str]
    editor: Optional[str]
    description: Optional[str]
    image_link: Optional[str]

@strawberry.type
class BookResponse:
    books: List[BookTypeEntity]
    source: Optional[str]
@strawberry.type
class BaseResponseDTO:
    api_version: str
    method: str
    data: BookResponse



