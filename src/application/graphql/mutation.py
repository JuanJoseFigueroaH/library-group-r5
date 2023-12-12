import strawberry
from src.application.entryPoint import deleteBook
@strawberry.type
class Mutation:
    
    @strawberry.mutation
    async def delete_book(self, bookId: int) -> str:
        return await deleteBook(bookId)