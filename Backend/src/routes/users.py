from fastapi import APIRouter, status, HTTPException, Request

from Backend.src.analytics_manager.user_engagement import user_activities
from Backend.src.persistant_db.db_manager import UsersTable

router = APIRouter(prefix="/users")


@router.get("")
def get_users(page: int = 1, pagesize: int = 1):
    users_table = UsersTable()
    return users_table.get_all_users(page=page, page_size=pagesize)


@router.get("/{user_id}")
def get_user(user_id: int):
    users_table = UsersTable()
    user = users_table.get_single_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user



