from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from typing import Optional, List
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

class Product(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    price: float
    embedding: Optional[list] = Field(sa_column=Column(Vector(3072)))