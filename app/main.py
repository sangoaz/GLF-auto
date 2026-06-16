from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.database import engine
from app.routes.auth import router as auth_router

from app.routes.admin_messages import router as admin_messages_router
from app.routes.admin_parts import router as admin_parts_router
from app.routes.admin_services import router as admin_services_router
from app.routes.admin_vehicles import router as admin_vehicles_router
from app.routes.public_contact import router as public_contact_router
from app.routes.public_parts import router as public_parts_router
from app.routes.public_services import router as public_services_router
from app.routes.public_trade_in import router as public_trade_in_router
from app.routes.public_vehicles import router as public_vehicles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)

# Configuration du limiter d'envoie de formulaire grâce à slowapi
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Branchement du dossier des photos uploadés
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://glf-auto.vercel.app",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# Branchement des différentes routes du dossier routes
app.include_router(auth_router)
app.include_router(admin_messages_router)
app.include_router(admin_parts_router)
app.include_router(admin_services_router)
app.include_router(admin_vehicles_router)
app.include_router(public_contact_router)
app.include_router(public_parts_router)
app.include_router(public_services_router)
app.include_router(public_trade_in_router)
app.include_router(public_vehicles_router)
