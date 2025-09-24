from fastapi import FastAPI, Request
from sqlmodel import SQLModel
from src.db import engine
from src.routes.product import router as product_router
from src.routes.user import router as user_router
from src.routes.chat import router as chat_router
from src.routes.shop import router as shop_router
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "year": datetime.now().year})

# Include routers
app.include_router(product_router)
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(shop_router)
