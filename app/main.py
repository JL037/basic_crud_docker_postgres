from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import bats


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(bats.router)
