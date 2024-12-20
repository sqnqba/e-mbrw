import datetime as dt
import uuid

from pydantic import EmailStr, PositiveInt, computed_field
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    ora_id: str | None = Field(unique=True, default=None, index=True, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    oso_kod: str | None = Field(default=None, min_length=6, max_length=6)
    fir_kod: str = Field(default="C000", min_length=4, max_length=4)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    ora_id: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
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
    fir_kod: str = Field(default="C000", min_length=4, max_length=4)
    comment: str | None = Field(default=None, max_length=1024)


# Properties to receive on order creation
class OrderCreate(OrderBase):
    kh_kod: str = Field(default="000000", min_length=6, max_length=6)


# Properties to receive on order update
class OrderUpdate(OrderBase):
    kh_kod: str = Field(default="000000", min_length=6, max_length=6)


# Database model, database table inferred from class name
class Order(OrderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    safo_id: PositiveInt | None = Field(default=None, index=True)
    safo_nr: PositiveInt | None = Field(default=None, index=True)
    kh_kod: str = Field(default="000000", min_length=6, max_length=6)
    kh_naz: str = Field(default="", max_length=512)
    created_at: dt.datetime = Field(default=dt.datetime.now(), nullable=False)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="orders")
    order_items: list["OrderItem"] = Relationship(
        back_populates="order", cascade_delete=True
    )

    @computed_field(return_type=float)
    @hybrid_property
    def value(self) -> float:
        return sum(
            order_item.product.price * order_item.quantity
            for order_item in self.order_items
        )

    class Config:
        arbitrary_types_allowed = True


# Properties to return via API, id is always required
class OrderPublic(OrderBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: dt.datetime
    value: float
    kh_kod: str
    # kh_naz: str


class OrdersPublic(SQLModel):
    data: list[OrderPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class ProductFeatureLink(SQLModel, table=True):
    product_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        foreign_key="product.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    feature_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, foreign_key="feature.id", primary_key=True
    )


class ProductBase(SQLModel):
    code: str = Field(unique=True, max_length=6)
    index: str = Field(default="", max_length=512)
    name: str = Field(default="", max_length=4096)
    full_name: str = Field(default="", max_length=512)
    is_shallow: bool = Field(default=False)
    parent_code: str | None = Field(default=None, max_length=6)
    price: float = Field(default=0.0)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_items: list["OrderItem"] = Relationship(back_populates="product")
    price_updated_at: dt.date | None = Field(
        default_factory=lambda: dt.datetime.now(),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: dt.datetime.now(),
        },
    )
    features: list["Feature"] | None = Relationship(
        back_populates="products", link_model=ProductFeatureLink
    )


class ProductPublic(ProductBase):
    # id: uuid.UUID
    features: list["Feature"] | None = Field(default=None)


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int


class Feature(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    feature_name: str = Field(default="", max_length=64, unique=True)
    feature_value: str = Field(default="", max_length=128, unique=True)

    products: list["Product"] = Relationship(
        back_populates="features", link_model=ProductFeatureLink
    )


class OrderItemBase(SQLModel):
    order_id: uuid.UUID
    product_id: uuid.UUID
    quantity: float


class OrderItem(OrderItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    order_id: uuid.UUID = Field(
        foreign_key="order.id", nullable=False, ondelete="CASCADE"
    )
    order: Order = Relationship(back_populates="order_items")
    product_id: uuid.UUID = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="order_items")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(SQLModel):
    product_id: uuid.UUID
    quantity: float


class OrderItemPubic(SQLModel):
    id: uuid.UUID
    order_id: uuid.UUID
    product: Product
    quantity: float


class OrderItemsPublic(SQLModel):
    data: list[OrderItemPubic]
    count: int


class Client(SQLModel):
    kod: str | None = None
    naz_s: str | None = None
    naz: str | None = None
    nip: str | None = None
    adr_k: str | None = None
    adr_m: str | None = None
    adr_u: str | None = None
    adr_d: str | None = None


class Clients(SQLModel):
    data: list[Client]
    count: int
