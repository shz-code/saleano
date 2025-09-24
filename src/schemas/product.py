from sqlmodel import SQLModel
from typing import List, Optional
from uuid import UUID

class ProductResponse(SQLModel):
    id: UUID
    name: str
    description: str
    price: float
    shop_id: UUID

class CreateProductRequest(SQLModel):
    name: str
    description: str
    price: float
    shop_id: UUID

class ProductSearchResponse(SQLModel):
    name: str
    price: float
    description: str

class ProductWithShopResponse(SQLModel):
    id: UUID
    name: str
    description: str
    price: float
    shop: "ShopResponse"

from .shop import ShopResponse
ProductWithShopResponse.update_forward_refs()