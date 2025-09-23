from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List

from src.models.product import Product
from src.db import get_session
from src.lib.gemini import get_embedding
from src.schemas.product import ProductResponse, CreateProductRequest, ProductSearchResponse
from src.constants import API_VERSION

router = APIRouter(prefix=f"/api/{API_VERSION}/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()

@router.post("/", response_model=CreateProductRequest)
def create_product(product: CreateProductRequest, session: Session = Depends(get_session)):
    embedding = get_embedding(product.name + " " + product.description)

    db_product = Product(
        **product.dict(),
        embedding=embedding
    )

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return product

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