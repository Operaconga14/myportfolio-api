from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from api.core.config.config import settings
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from api.v1.endpoints import admin

app = FastAPI()

# Cors Middleware Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# @app.on_event("startup")
# async def startup():
#     # register_tortoise(
#     #     app=app,
#     #     config=settings.DB_CONFIG,
#     #     generate_schemas=True,
#     #     add_exception_handlers=True
#     # )

register_tortoise(
    app,
    db_url="sqlite://test.db",
    modules={"models": ["api.models.model"]},
    add_exception_handlers=True,
    generate_schemas=True
)


@app.get('/')
def read_root():
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"{settings.Messages.get('success').get('welcome')}")


# Api router
app.include_router(
    admin.router, prefix=f"{settings.API_VI_STR}/admin", tags=['Admin'])
