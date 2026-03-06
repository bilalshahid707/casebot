from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    detail: str = "An unexpected error occurred"
