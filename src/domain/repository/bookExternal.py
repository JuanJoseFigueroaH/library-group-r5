from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Coroutine
from src.domain.entity import BookEntity, BookFilter, BookDTOEntity, SourceEntity
from dependency_injector.providers import Configuration
from src.infrastructure import IHttpClient
from asyncio import gather
from json import loads
import hashlib
import logging


class IBookExternalRepository(ABC):
    @abstractmethod
    async def get_books(self, filters: BookFilter) -> BookDTOEntity:
        raise NotImplementedError
    

class BookExternalRepository(IBookExternalRepository):
    def __init__(
        self, 
        http_client: IHttpClient,
        configuration: Configuration
    ):
        self._http_client = http_client
        self._log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self._base_url_google_books = (
            configuration["api"]["google"]["base_url"]
        )
        self._base_url_open_libra = (
            configuration["api"]["open"]["base_url"]
        )
    
    async def get_books(self, filters: BookFilter) -> BookDTOEntity:
        async_calls: List[Coroutine[Any, Any, List[BookEntity]]] = list()
        async_calls.append(self._get_books_of_google_books(filters))
        async_calls.append(self._get_books_of_open_libra(filters))
        all_results = await gather(*async_calls)
        
        books = [book for books in all_results for book in books]
        return BookDTOEntity(books=books, source=SourceEntity.external)
    
    async def _get_books_of_google_books(self, filters: BookFilter) -> List[BookEntity]:
        print("Books Google")
        books: List[BookEntity] = list()
        filtered_mappers = list()
        print(filters)
        if filters.title:
            filtered_mappers.append(f"intitle:{filters.title}")
            
        if filters.author:
            filtered_mappers.append(f"inauthor:{filters.author}")
            
        if filters.editor:
            filtered_mappers.append(f"inpublisher:{filters.editor}")
            
        if not filtered_mappers:
            return books
            
        url_filtered = f"?fields=items(volumeInfo)&q={'+'.join(filtered_mappers).replace(' ', '%20')}"
        print(url_filtered)
        try:
            print("Entro petición")
            http_data, http_status = (
                await self._http_client.get(f"{self._base_url_google_books}{url_filtered}")
            )
        except Exception as error:
            self._log.exception(
                "An error occurred while trying to query the external data repository",
                exc_info=error
            )
            return books
        print(http_status)
        if http_status == 200:
            result = loads(http_data)
            for book in result.get("items", []):
                volumeInfo: Dict[str, Any] = book["volumeInfo"]
                entity = BookEntity(
                    title = str(volumeInfo["title"]).lower() if volumeInfo.get("title") else None,
                    subtitle = str(volumeInfo["subtitle"]).lower() if volumeInfo.get("subtitle") else None,
                    description = str(volumeInfo["description"]).lower() if volumeInfo.get("description") else None,
                    editor = str(volumeInfo["publisher"]).lower() if volumeInfo.get("publisher") else None,
                    authors = set(
                        [str(a).lower() for a in volumeInfo["authors"]] 
                        if volumeInfo.get("authors", set())
                        else []
                    ),
                    categories = set(
                        [str(a).lower() for a in volumeInfo["categories"]] 
                        if volumeInfo.get("categories", set()) 
                        else []
                    ),
                )
                datetime_publication = volumeInfo.get("publishedDate")
                entity.datetime_publication = (
                    None
                    if not datetime_publication
                    else str(datetime_publication[0:4])
                )
                image_link: Optional[Dict[str, str]] = volumeInfo.get("imageLinks")
                entity.image_link = (
                    None
                    if not image_link
                    else str(list(image_link.values())[-1])
                )
                _identified = f"{entity.title}-{entity.subtitle}-{entity.authors.__str__()}-{entity.datetime_publication}"
                entity.id = hashlib.sha256(_identified.encode()).hexdigest()

                books.append(entity)

        return books
        
    async def _get_books_of_open_libra(self, filters: BookFilter) -> List[BookEntity]:
        books: List[BookEntity] = list()
        filtered_mappers = list()
        
        if filters.title:
            filtered_mappers.append(f"book_title={filters.title}")
            
        if filters.author:
            filtered_mappers.append(f"book_author={filters.author}")
            
        if filters.editor:
            filtered_mappers.append(f"publisher={filters.editor}")
            
        if filters.category:
            filtered_mappers.append(f"category={filters.category}")
            
        if filters.datetime_publication:
            filtered_mappers.append(f"publisher_date={filters.datetime_publication}")
            
        if not filtered_mappers:
            return books
            
        url_filtered = f"{self._base_url_open_libra}?{'&'.join(filtered_mappers).replace(' ', '%20')}"
        try:
            http_data, http_status = (
                await self._http_client.get(url_filtered)
            )
        except Exception as error:
            self._log.exception(
                "An error occurred while trying to query the external data repository",
                exc_info=error
            )
            return books
        
        if http_status == 200:
            result = loads(http_data)
            for book in result:
                entity = BookEntity(
                    title = str(book["title"]).lower() if book.get("title") else None,
                    subtitle = str(book["subtitle"]).lower() if book.get("subtitle") else None,
                    description = str(book["content"]).lower() if book.get("content") else None,
                    editor = str(book["publisher"]).lower() if book.get("publisher") else None,
                    image_link = book.get("thumbnail"),
                )
                datetime_publication = book.get("publisher_date")
                entity.datetime_publication = (
                    None
                    if not datetime_publication
                    else str(datetime_publication[0:4])
                )
                categories = book.get("categories", set())
                entity.categories = (
                    set()
                    if not categories
                    else set([str(category["name"]).lower() for category in categories])
                )
                authors = book.get("author")
                entity.authors = (
                    set()
                    if not authors
                    else set([str(authors).lower()])
                )
                _identified = f"{entity.title}-{entity.subtitle}-{entity.authors.__str__()}-{entity.datetime_publication}"
                entity.id = hashlib.sha256(_identified.encode()).hexdigest()
                
                books.append(entity)

        return books
