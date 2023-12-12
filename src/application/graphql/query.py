from typing import List

import strawberry
from dependency_injector.wiring import inject
from src.application.graphql.schema import BookType

@strawberry.type
class Query:
    @strawberry.field
    @inject
    async def get_all_book(self) -> List[BookType]:
        pass