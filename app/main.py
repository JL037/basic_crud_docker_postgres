from fastapi import FastAPI
from app.database import Base, engine
from app.models import bats
from app.routers import bats
from app.routers import auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(bats.router)
app.include_router(auth_router.router)