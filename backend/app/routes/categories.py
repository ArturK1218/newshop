from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.category_service import CatgoryService
from app.schemas.category import CategoryResponseSchema


router = APIRouter(
    prefix="/api/categories",
    tags=["categories"]
)

@router.get("", response_model=List[CategoryResponseSchema], status_code=status.HTTP_200_OK)
def get_categories(db:Session = Depends(get_db)):
    service = CatgoryService(db)
    return service.get_all_categories()

@router.get("/{category_id}", response_model=CategoryResponseSchema, status_code=status.HTTP_200_OK)
def get_category(category_id: int, db: Session = Depends(get_db)):
    service = CatgoryService(db)
    return service.get_category_by_id(category_id)