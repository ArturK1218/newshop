from pydantic import BaseModel, Field

class CategoryBaseSchema(BaseModel):
    name: str = Field(..., min_length=5, max_length=100,
                      description="Category name")
    slug: str = Field(..., min_length=5, max_length=100,
                      description="URL category name")
    
class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryResponseSchema(CategoryBaseSchema):
    id: int = Field(..., description="Inque category identifier")

    class Config:
        from_attributes = True