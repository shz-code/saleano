from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from src.models.product import Product
from src.models.shop import Shop
from src.db import get_session
from src.lib.gemini import get_embedding
from src.schemas.product import ProductResponse, CreateProductRequest, ProductSearchResponse, ProductWithShopResponse
from src.constants import API_VERSION

router = APIRouter(prefix=f"/api/{API_VERSION}/products", tags=["Products"])

@router.get("/", response_model=List[ProductWithShopResponse])
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@router.post("/", response_model=ProductResponse)
def create_product(product: CreateProductRequest, session: Session = Depends(get_session)):
    # Validate that the shop exists
    shop = session.exec(select(Shop).where(Shop.id == product.shop_id)).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    embedding = get_embedding(product.name + " " + product.description)

    db_product = Product(
        **product.dict(),
        embedding=embedding
    )

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/search", response_model=List[ProductSearchResponse])
def search_products(q: str, limit: int = 10, session: Session = Depends(get_session)):
    query_embedding = get_embedding(q)

    # Query only name and price
    stmt = (
        select(Product.name, Product.price, Product.description)
        .order_by(Product.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )

    results = session.exec(stmt).all()

    return results