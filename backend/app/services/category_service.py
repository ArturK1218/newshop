from sqlalchemy.orm import Session
from typing import List
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryResponseSchema, CategoryCreateSchema
from fastapi import HTTPException, status


class CatgoryService:
    def __init__(self, db: Session):
        self.repostiry = CategoryRepository(db)

    def get_all_categories(self) ->List[CategoryResponseSchema]:
        categories = self.repostiry.get_all()
        return [CategoryResponseSchema.model_validate(cat) for cat in categories]
    
    def get_category_by_id(self, category_id: int) -> CategoryResponseSchema:
        category = self.repostiry.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Category with id {category_id} not found'
            )
        
        return CategoryResponseSchema.model_validate(category)
    
    def create_category(self, category_data: CategoryCreateSchema) -> CategoryResponseSchema:
        category = self.repostiry.create(category_data)
        return CategoryResponseSchema.model_validate(category)