from fastapi import APIRouter

from app.api.routes import clients, login, orders, product, users, utils

api_router = APIRouter()
api_router.include_router(product.router, prefix="/products", tags=["products"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
