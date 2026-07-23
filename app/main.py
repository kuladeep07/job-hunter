from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from beanie import init_beanie
from fastapi import FastAPI
from contextlib import asynccontextmanager

from pymongo import AsyncMongoClient

from app.core.configs.settings import settings
from app.models.ProcessedJobs import ProcessedJobs
from app.models.Resumes import Resumes
from app.models.Shortlists import Shortlists
from app.routers.resumes import resumes_router

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient(str(settings.db_url))
    database = client[str(settings.database_name)]

    await init_beanie(database=database, document_models=[ProcessedJobs, Resumes, Shortlists])

    app.state.mongo_client = client
    print("connected to db")

    scheduler.start()

    yield

    await client.aclose()
    print("mongodb connection closed")
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(resumes_router)
