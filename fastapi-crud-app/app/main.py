from fastapi import FastAPI
from app.db.database import Base, engine
from app.api import user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router) 
from app.api import user_routes