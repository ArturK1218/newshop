from pydantic import BaseModel, Field
from typing import Optional


class CartItemBaseSchema(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity (must be grater then zero)")

class CartItemCreateSchema(CartItemBaseSchema):
    pass 

class CartItemUpdateSchema(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, 
                          description="Quantity (must be grater then zero)")

class CartItem(BaseModel):
    product_id: int
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    quantity: int = Field(..., description="Quantity of items in cart")
    subtotal: float = Field(..., 
                            description="Total price for this item (item + quantity)")
    image_url: Optional[str] = Field(None, description="Product image URL")

class CartResponseSchema(BaseModel):
    items: list[CartItem] = Field(..., description="List of items in cart")
    total: float = Field(..., description="Total cart price")
    items_count: int = Field(..., description="Total number of items in cart")
    