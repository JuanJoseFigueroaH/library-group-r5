from src.domain.entity import BookFilter, SourceEntity, BaseResponseDTO
from typing import Optional
from fastapi import APIRouter, status, Depends, Response, BackgroundTasks
from dependency_injector.wiring import inject, Provide
from src.infrastructure.container import Container
from src.domain.service import BookService, IBookService

@inject
async def getBook(
    id: Optional[str]=None,
    title: Optional[str]=None, 
    subtitle: Optional[str]=None,
    author: Optional[str]=None,
    category: Optional[str]=None,
    datetime_publication: Optional[str]=None,
    editor: Optional[str]=None,
    description: Optional[str]=None,
    service: IBookService=Depends(Provide[Container.service_book])
):
    books = await service.get_books(
        BookFilter(
            id=id,
            title=title,
            subtitle=subtitle,
            author=author,
            category=category,
            datetime_publication=datetime_publication,
            editor=editor,
            description=description,
        )
    )
    
    if books.source == SourceEntity.external:
        await service.save_books_external(books.books)
        
    return BaseResponseDTO(
        statusCode="200", 
        message="Successfully get book",
        data=books
    )

@inject
async def deleteBook(
    id: str,
    service: IBookService=Depends(Provide[Container.service_book])
):
    await service.delete_book(id)
    return BaseResponseDTO(
        statusCode="200", 
        message="Successfully deleted book",
        data=id
    )