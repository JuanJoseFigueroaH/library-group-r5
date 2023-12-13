import strawberry
from src.application.entryPoint import deleteBook
from src.application.graphql.schema import BaseResponseDeleteDTO
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def delete_book(self, bookId: str) -> BaseResponseDeleteDTO:
        return await deleteBook(bookId)