from sqlalchemy.orm import Session
from typing import Dict
from app.repositories.product_repository import ProductRepsitory
from app.schemas.cart import CartResponseSchema, CartItem, \
      CartItemCreateSchema, CartItemUpdateSchema
from fastapi import HTTPException, status


class CartService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepsitory(db)

    def add_to_cart(self, cart_data: Dict[int, int], item: CartItemCreateSchema) -> Dict[int, int]:
        product = self.product_repository.get_by_id(item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {item.product_id} not found'
            )
        
        if item.product_id in cart_data:
            cart_data[item.product_id] += item.quantity
        else:
            cart_data[item.product_id] = item.quantity

        return cart_data
    
    def update_cart_item(self, cart_data: Dict[int, int], item: CartItemUpdateSchema) -> Dict[int, int]:
        if item.product_id not in cart_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {item.product_id} not found in cart'
            )
        
        cart_data[item.product_id] = item.quantity
        return cart_data
    
    def remove_from_cart(self, cart_data: Dict[int, int], product_id: int) -> Dict[int, int]:
        if product_id not in cart_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product with id {product_id} not found in cart'
            )
        
        del cart_data[product_id]
        return cart_data
    
    def get_cart_detail(self, cart_data: Dict[int, int]) -> CartResponseSchema:
        if not cart_data:
            return CartResponseSchema(items=[], total=0, items_count=0)
        
        product_ids = list(cart_data.keys())
        products = self.product_repository.get_multiple_by_ids(product_ids)
        products_dict = {product.id: product for product in products}

        cart_items = []
        total_price = 0.0
        total_items = 0

        for product_id, quantity in cart_data.items():
            if product_id in products_dict:
                product = products_dict[product_id]
                subtotal = product.price * quantity

                cart_item = CartItem(product_id=product.id, name=product.name,
                                     price=product.price, quantity=product.quantity, subtotal=subtotal,
                                     image_url=product.image_url)
                
                cart_items.append(cart_item)
                total_price += subtotal
                total_items += quantity

                return CartResponseSchema(items=cart_items, total=round(total_price),
                                          items_count=total_items)
            