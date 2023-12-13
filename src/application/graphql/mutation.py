import strawberry
from src.application.entryPoint import deleteBook
@strawberry.type
class Mutation:
    
    @strawberry.mutation
    async def delete_book(self, bookId: str) -> str:
        return await deleteBook(bookId)