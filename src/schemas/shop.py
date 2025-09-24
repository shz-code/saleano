from sqlmodel import SQLModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ShopResponse(SQLModel):
    id: UUID
    name: str
    description: Optional[str]
    tags: Optional[str]
    created_at: datetime
    updated_at: datetime

class CreateShopRequest(SQLModel):
    name: str
    description: Optional[str] = None
    tags: Optional[str] = None  # JSON string

class ShopWithProductsResponse(SQLModel):
    id: UUID
    name: str
    description: Optional[str]
    tags: Optional[str]
    created_at: datetime
    updated_at: datetime
    products: List["ProductResponse"]

from .product import ProductResponse
ShopWithProductsResponse.update_forward_refs()