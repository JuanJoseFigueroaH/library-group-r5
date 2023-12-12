import strawberry

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def delete_book(self, book_id: int) -> str:
        pass