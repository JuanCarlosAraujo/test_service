from fastapi import FastAPI
from client_management.urls import user 
from config.open_api import tags_metadata
from client_management.urls import user as user_router

app = FastAPI(
    title="Users API",
    description="a REST API using python and mysql",
    version="0.0.1",
    openapi_tags=tags_metadata,

)

app.include_router(user_router, prefix="/users")

