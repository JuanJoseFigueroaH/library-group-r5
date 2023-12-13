from abc import ABC, abstractmethod
from src.domain.entity import BookEntity, BookFilter, BookDTOEntity
from src.domain.repository import IBookRepository, IBookExternalRepository
from typing import List
import logging

class IBookService(ABC):
    @abstractmethod
    async def get_books(self, filter: BookFilter) -> BookDTOEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def save_books_external(self, books: List[BookEntity]):
        raise NotImplementedError

    @abstractmethod
    async def delete_book(self, id: str):
        raise NotImplementedError

class BookService(IBookService):   
    def __init__(
        self, 
        book_repository: IBookRepository,
        book_external_repository: IBookExternalRepository
    ):
        self._book_repository = book_repository
        self._book_external_repository = book_external_repository
        self._log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def get_books(self, filter: BookFilter) -> BookDTOEntity:
        internal_book = await self._book_repository.getBook(filter)
        if internal_book.books:
            return internal_book
        external_book = await self._book_external_repository.get_books(filter)
        print(external_book)
        if external_book.books:
            return external_book
        
        
        return BookDTOEntity(books=list(), source=None)
    
    async def save_books_external(self, books: List[BookEntity]):
        self._log.info("Initialize background task- save books of source external")
        for book in books:
            await self._book_repository.save_book(book)
        self._log.info("Finished background task - save books of source external")
    
    async def delete_book(self, id: str):
        if not id:
            return
        await self._book_repository.delete_book(id)