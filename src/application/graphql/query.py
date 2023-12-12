from typing import List, Optional
import strawberry
from dependency_injector.wiring import inject, Provide
from src.application.graphql.schema import BookType, BaseResponseDTO
from src.application.entryPoint import getBook
@strawberry.type
class Query:
    @strawberry.field
    async def get(
        self,
        id: Optional[str] = None,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        author: Optional[str] = None,
        category: Optional[str] = None
    )-> BaseResponseDTO:
        return await getBook(id, title, subtitle, author, category)