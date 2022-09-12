from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    # to convert orm response to dict and pydantic model
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str

    # def __init__(self, **data: Any):
    #     data["password"] = utils.get_hash(data["password"])
    #     super().__init__(**data)


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None


class Product(BaseModel):
    id: int
    name: str
    manufacturer: str
    supplier: str
    category: str
    sub_category: str
    country_of_origin: str
    created_at: datetime
    updated_at: datetime

    # to convert orm response to dict and pydantic model
    class Config:
        orm_mode = True


class InventoryProduct(BaseModel):
    id: int
    name: str
    manufacturer: str
    supplier: str
    category: str
    sub_category: str
    country_of_origin: str
    inventory_count: int
    created_at: datetime
    updated_at: datetime

    # to convert orm response to dict and pydantic model
    class Config:
        orm_mode = True


class Cart(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    # to convert orm response to dict and pydantic model
    class Config:
        orm_mode = True


class AddToCart(BaseModel):
    product_id: int
    quantity: int

    # to convert orm response to dict and pydantic model
    class Config:
        orm_mode = True


class UpdateCart(BaseModel):
    quantity: int

    # to convert orm response to dict and pydantic model
    class Config:
        orm_mode = True


class CartProductOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    product: Product

    # to convert orm response to dict and pydantic model
    class Config:
        orm_mode = True
