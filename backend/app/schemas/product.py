from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.category import CategoryResponseSchema


class ProductBaseSchema(BaseModel):
    name: str = Field(..., min_length=5, max_length=100,
                      description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0,
                         description="Product price(must be greater then zero!)")
    category_id: int = Field(..., description="Category ID")
    image_url: Optional[str] = Field(None, description="Image URL")

class ProductCreateSchema(ProductBaseSchema):
    pass 

class ProductResponseSchema(BaseModel):
    id: int = Field(..., description="Unique product ID")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    category: CategoryResponseSchema = Field(..., description="Product category details")

    class Config:
        from_attributes = True

class ProductListResponseSchema(BaseModel):
    products: list[ProductResponseSchema]
    total: int = Field(..., description='Total')