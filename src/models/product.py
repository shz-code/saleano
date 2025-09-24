from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, List, TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

if TYPE_CHECKING:
    from .shop import Shop

class Product(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    price: float
    shop_id: UUID = Field(foreign_key="shop.id")
    embedding: Optional[list] = Field(sa_column=Column(Vector(3072)))

    # Relationship back to shop
    shop: Optional["Shop"] = Relationship(back_populates="products")