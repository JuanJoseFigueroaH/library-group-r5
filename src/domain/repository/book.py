from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entity import BookEntity, SourceEntity, BookFilter, BookDTOEntity
from src.infrastructure import IPostgresContext
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy import or_, delete, func
from src.domain.model import Book, Editor, Author, Category
from src.infrastructure import IPostgresContext
import logging

class IBookRepository(ABC):
    @abstractmethod
    async def getBook(self, filters: BookFilter) -> BookDTOEntity:
        raise NotImplementedError

class BookRepository(IBookRepository):
    def __init__(self, context: IPostgresContext):
        self._context = context
        self._log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
    
    async def getAllBookBySession(self, query):
        async with self._context.create_session() as session:
            data = await session.execute(query)
            return data.all()

    async def getBook(self, filters: BookFilter) -> BookDTOEntity:
        books = BookDTOEntity(books=list(), source=SourceEntity.internal)
        alias_author: Author = aliased(Author)
        alias_category: Category = aliased(Category)
        alias_editor: Editor = aliased(Editor)
        query = (
            select(Book)
            .options(selectinload(Book.editor))
            .options(selectinload(Book.authors))
            .options(selectinload(Book.categories))
            .join(alias_author, Book.authors, isouter=True)
            .join(alias_category, Book.categories, isouter=True)
            .join(alias_editor, Book.editor, isouter=True)
            .distinct(Book.id)
        )

        any_criterian = list()
        
        if filters.id:
            any_criterian.append(func.lower(Book.id).like(f"%{filters.id.lower()}%"))
            
        if filters.title:
            any_criterian.append(func.lower(Book.title).like(f"%{filters.title.lower()}%"))
            
        if filters.subtitle:
            any_criterian.append(func.lower(Book.subtitle).like(f"%{filters.subtitle.lower()}%"))
            
        if filters.description:
            any_criterian.append(func.lower(Book.description).like(f"%{filters.description.lower()}%"))
            
        if filters.datetime_publication:
            any_criterian.append(Book.editor_date == filters.datetime_publication)
            
        if filters.author:
            any_criterian.append(func.lower(alias_author.name).like(f"%{filters.author.lower()}%"))
            
        if filters.category:
            any_criterian.append(func.lower(alias_category.name).like(f"%{filters.category.lower()}%"))
            
        if filters.editor:
            any_criterian.append(func.lower(alias_editor.name).like(f"%{filters.editor.lower()}%"))
            
        if not any_criterian:
            return books
        
        query = query.where(or_(*any_criterian))

        try:
            result = await self.getAllBookBySession(query)
        except Exception as error:
            self._log.exception(
                "An error occurred while trying to query the data repository",
                exc_info=error
            )
            return books
        
        if result:
            book_list: List[BookEntity] = list()
            for row in result:
                _book: Book = row[0]
                book = BookEntity(
                    id = _book.id,
                    title = _book.title,
                    subtitle = _book.subtitle,
                    description = _book.description,
                    datetime_publication = _book.editor_date,
                    image_link = _book.image,
                )
                if _book.editor:
                    book.editor = _book.editor.name
                    
                if _book.authors:
                    book.authors = set([author.name for author in _book.authors])
                    
                if _book.categories:
                    book.categories = set([category.name for category in _book.categories])
                book_list.append(book)
            books.books = book_list
        
        return books
    
    async def save_book(self, book: BookEntity):
        try:
            async with self._context.create_session() as session:
                editor: Optional[Editor] = None
                authors: List[Author] = list()
                categories: List[Category] = list()
                async with session.begin():
                    if book.editor:
                        if editor_exists := (await session.execute(select(Editor).where(Editor.name == book.editor))).one_or_none():
                            editor = editor_exists[0]
                        else:
                            editor = Editor(name=book.editor)
                            session.add(editor)
                        
                    if book.authors:
                        authors: List[Author] = list()
                        for author in book.authors:
                            if author_exists := (await session.execute(select(Author).where(Author.name == author))).one_or_none():
                                authors.append(author_exists[0])
                            else:
                                author = Author(name=author)
                                authors.append(author)
                                session.add(author)
                        
                    if book.categories:
                        categories: List[Category] = list()
                        for category in book.categories:
                            if category_exists := (await session.execute(select(Category).where(Category.name == category))).one_or_none():
                                categories.append(category_exists[0])
                            else:
                                category = Category(name=category)
                                categories.append(category)
                                session.add(category)
                        
                async with session.begin():
                    _book = Book(
                        id=book.id,
                        title=book.title,
                        subtitle=book.subtitle,
                        description=book.description,
                        editor_date=book.datetime_publication,
                        image=book.image_link,
                        editor=editor,
                        authors=authors,
                        categories=categories
                    )
                    session.add(_book)
        except Exception as error:
            self._log.exception(
                "An error occurred while trying to persist in the data repository",
                exc_info=error
            )
            return
    