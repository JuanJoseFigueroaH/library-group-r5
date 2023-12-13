from typing import Any, Optional
from pydantic import BaseModel

class BaseResponseDTO(BaseModel):
    statusCode : str
    message: str
    data: Optional[Any]