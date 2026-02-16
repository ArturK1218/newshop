from sqlalchemy.orm import Session
from typing import List
from app.repositories.product_repository import ProductRepsitory
from app.repositories.category_repository import CategoryRepository
from app.schemas.product import ProductResponseSchema, ProductListResponseSchema, ProductCreateSchema
from fastapi import HTTPException, status


class ProductService:
    def __init__(self, db: Session):
        self.product_repositry = ProductRepsitory(db)
        self.category_repository = CategoryRepository(db)

    def get_all_products(self) -> ProductListResponseSchema:
        products = self.product_repositry.get_all()
        products_response = [ProductResponseSchema.model_validate(prod) for prod in products]
        return ProductListResponseSchema(products=products_response, total=len(products_response))
    
    def get_product_by_id(self, product_id: int) -> ProductResponseSchema:
        product = self.product_repositry.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {product_id} not found'
            )
        
        return ProductResponseSchema.model_validate(product)
    
    def get_product_by_category(self, category_id: int) -> ProductListResponseSchema:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Category with id {category_id} not found'
            )
        
        products = self.product_repositry.get_by_category(category_id)
        products_response = [ProductResponseSchema.model_validate(prod) for prod in products]
        return ProductListResponseSchema(products=products_response, total=len(products_response))
    
    def create_product(self, product_data: ProductCreateSchema) -> ProductResponseSchema:
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail=f'Catgory with id {product_data.category_id} does not exist'
            )
        
        product = self.product_repositry(product_data)
        return ProductResponseSchema.model_validate(product)
    
