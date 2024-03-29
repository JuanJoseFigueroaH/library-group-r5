from typing import Optional
from pydantic import BaseModel

class BookFilter(BaseModel):
    id: Optional[str]
    title: Optional[str] 
    subtitle: Optional[str]
    author: Optional[str]
    category: Optional[str]
    datetime_publication: Optional[str]
    editor: Optional[str]
    description: Optional[str]

