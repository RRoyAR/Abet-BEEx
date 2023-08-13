from fastapi import APIRouter, status, HTTPException, Request

from Backend.src.analytics_manager.user_engagement import user_activities
from Backend.src.persistant_db.db_manager import ProductsTable

router = APIRouter(prefix="/products")

@router.get("")
def get_users(page: int = 1, pagesize: int = 1):
    product_table = ProductsTable()
    return product_table.get_all_products(page=page, page_size=pagesize)


@router.get("/{product_id}")
def get_user(product_id: int):
    product_table = ProductsTable()
    product = product_table.get_single_product(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return product