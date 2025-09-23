from sqlmodel import SQLModel
from typing import List
from uuid import UUID

class ProductResponse(SQLModel):
    id: UUID
    name: str
    description: str
    price: float

class CreateProductRequest(SQLModel):
    name: str
    description: str
    price: float

class ProductSearchResponse(SQLModel):
    name: str
    price: float
    description: str