import uuid
from ast import List
from re import L

from pydantic import EmailStr, PositiveInt
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    ora_id: str | None = Field(unique=True, default=None, index=True, max_length=255)
    email: EmailStr = Field(index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    oso_kod: str | None = Field(default=None, min_length=6, max_length=6)
    fir_kod: str | None = Field(default=None, min_length=4, max_length=6)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    orders: list["Order"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class OrderBase(SQLModel):
    safo_nr: PositiveInt | None = Field(default=None, index=True)
    kh_kod: str = Field(default="000000", min_length=6, max_length=6)
    # title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on order creation
class OrderCreate(OrderBase):
    pass


# Properties to receive on order update
class OrderUpdate(OrderBase):
    kh_kod: str = Field(default="000000", min_length=6, max_length=6)
    # title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Order(OrderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    safo_id: PositiveInt | None = Field(default=None, index=True)
    kh_kod: str = Field(default="000000", min_length=6, max_length=6)
    # title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="orders")
    items: list["OrderItem"] = Relationship(back_populates="order", cascade_delete=True)


# Properties to return via API, id is always required
class OrderPublic(OrderBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class OrdersPublic(SQLModel):
    data: list[OrderPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class Product(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str
    price: float
    orders: list["OrderItem"] = Relationship(back_populates="product")


class OrderItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(foreign_key="order.id")
    order: Order = Relationship(back_populates="items")
    product_id: uuid.UUID = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="orders")
    quantity: int
