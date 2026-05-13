from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.core.logger import logger

from app.api import auth, users, drivers, trailers, routes, trips, orders, analytics, audit_logs

from app.seed.seed_users import seed_users
from app.seed.seed_drivers import seed_drivers
from app.seed.seed_trailers import seed_trailers
from app.seed.seed_orders import seed_orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_users(db)
        seed_drivers(db)
        seed_trailers(db)
        seed_orders(db)
    finally:
        db.close()
    
    yield
    
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(drivers.router)
app.include_router(trailers.router)
app.include_router(routes.router)
app.include_router(trips.router)
app.include_router(orders.router)
app.include_router(analytics.router)
app.include_router(audit_logs.router)


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}