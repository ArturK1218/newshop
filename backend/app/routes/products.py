from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.product_service import ProductService
from app.schemas.product import ProductResponseSchema, ProductListResponseSchema


router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

@router.get("", response_model=ProductListResponseSchema, status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    services = ProductService(db)
    return services.get_all_products()

@router.get("/{product_id}", response_model=ProductResponseSchema, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_id(product_id)

@router.get("/category/{category_id}", response_model=ProductListResponseSchema, status_code=status.HTTP_200_OK)
def get_products_by_caegory(category_id: int, db: Session = Depends(get_db)):
    services = ProductService(db)
    return services.get_product_by_category(category_id)