import strawberry

@strawberry.type
class BookType:
    id: int
    title: str
    subtitle: str