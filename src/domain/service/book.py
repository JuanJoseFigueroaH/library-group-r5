from abc import ABC, abstractmethod
from src.domain.entity import BookEntity, BookFilter, BookDTOEntity
from src.domain.repository import IBookRepository
import logging

class IBookService(ABC):
    @abstractmethod
    async def get_books(self, filter: BookFilter) -> BookDTOEntity:
        raise NotImplementedError

class BookService(IBookService):   
    def __init__(
        self, 
        book_repository: IBookRepository
    ):
        self._book_repository = book_repository
        self._log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def get_books(self, filter: BookFilter) -> BookDTOEntity:
        internal_book = await self._book_repository.get_books(filter)
        if internal_book.books:
            return internal_book
        
        return BookDTOEntity(books=list(), source=None)