from fastapi import FastAPI
from fastapi.exception_handlers import http_exception_handler
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

from Backend.src.routes import users

app = FastAPI(title="AlfaBet BE Exercise", version="1.0.0")


@app.exception_handler(HTTPException)
async def exception_handler(request, exception):
    print(f"Returned status code: {exception.status_code} with detail: {exception.detail}")
    return await http_exception_handler(request, exception)

app.include_router(users.router, prefix="/api")
# app.include_router(database_main_route.router, prefix="/api/v1")

