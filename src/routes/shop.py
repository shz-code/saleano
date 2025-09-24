from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from src.models.shop import Shop
from src.db import get_session
from src.schemas.shop import ShopResponse, CreateShopRequest, ShopWithProductsResponse
from src.constants import API_VERSION

router = APIRouter(prefix=f"/api/{API_VERSION}/shops", tags=["Shops"])

@router.get("/", response_model=List[ShopResponse])
def get_shops(session: Session = Depends(get_session)):
    return session.exec(select(Shop)).all()

@router.post("/", response_model=ShopResponse)
def create_shop(shop: CreateShopRequest, session: Session = Depends(get_session)):
    # Check if shop with same name already exists
    existing_shop = session.exec(select(Shop).where(Shop.name == shop.name)).first()
    if existing_shop:
        raise HTTPException(status_code=400, detail="Shop with this name already exists")

    db_shop = Shop(**shop.dict())
    session.add(db_shop)
    session.commit()
    session.refresh(db_shop)
    return db_shop

@router.get("/{shop_id}", response_model=ShopWithProductsResponse)
def get_shop(shop_id: str, session: Session = Depends(get_session)):
    shop = session.exec(select(Shop).where(Shop.id == shop_id)).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop

@router.put("/{shop_id}", response_model=ShopResponse)
def update_shop(shop_id: str, shop_update: CreateShopRequest, session: Session = Depends(get_session)):
    shop = session.exec(select(Shop).where(Shop.id == shop_id)).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    # Check if another shop with the same name exists
    existing_shop = session.exec(
        select(Shop).where(Shop.name == shop_update.name, Shop.id != shop_id)
    ).first()
    if existing_shop:
        raise HTTPException(status_code=400, detail="Shop with this name already exists")

    for field, value in shop_update.dict().items():
        setattr(shop, field, value)

    session.commit()
    session.refresh(shop)
    return shop

@router.delete("/{shop_id}")
def delete_shop(shop_id: str, session: Session = Depends(get_session)):
    shop = session.exec(select(Shop).where(Shop.id == shop_id)).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    session.delete(shop)
    session.commit()
    return {"message": "Shop deleted successfully"}