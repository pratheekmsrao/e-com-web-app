import time

import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor

# from . import models
from .config import settings
# from .database import engine
from .routers import auth, cart, checkout, inventory, product, user

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# adding all app routes
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(inventory.router)
app.include_router(cart.router)
app.include_router(checkout.router)


@app.get("/")
def root():
    return {"message": "Hello World !!!"}


