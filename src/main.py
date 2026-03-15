from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from helpers.config import get_settings

settings = get_settings()  # load settings once

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    print("MongoDB connected")
    
    yield  # application runs after this

    # --- shutdown ---
    app.mongo_conn.close()
    print("MongoDB connection closed")

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)

