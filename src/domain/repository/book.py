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
    async def get_books(self, filters: BookFilter) -> BookDTOEntity:
        raise NotImplementedError

class BookRepository(IBookRepository):
    def __init__(self, context: IPostgresContext):
        self._context = context
        self._log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
    
    async def _get_all_books_by_session(self, query):
        async with self._context.create_session() as session:
            data = await session.execute(query)
            return data.all()

    async def get_books(self, filters: BookFilter) -> BookDTOEntity:
        books = BookDTOEntity(books=list(), source=SourceEntity.internal)
        alias_author: Author = aliased(Author)
        alias_category: Category = aliased(Category)
        alias_editor: Editor = aliased(Editor)
        query = (
            select(Book)
            .options(selectinload(Book.publisher))
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
            any_criterian.append(Book.publisher_date == filters.datetime_publication)
            
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
            result = await self._get_all_books_by_session(query)
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
    