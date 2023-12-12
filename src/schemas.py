import graphene

class BookType(graphene.ObjectType):
    id = graphene.String()
    title = graphene.String()
    subtitle = graphene.String()
    author = graphene.String()
    category = graphene.String()
    datetime_publication = graphene.String()
    editor = graphene.String()
    description = graphene.String()

class BooksQuery(graphene.ObjectType):
    get_books = graphene.List(BookType)

    def resolve_get_books(self, info, **kwargs):
        # Your logic to fetch books goes here
        pass

schema = graphene.Schema(query=BooksQuery)