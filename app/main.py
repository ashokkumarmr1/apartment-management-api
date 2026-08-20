from fastapi import FastAPI
from app.core.init_db import InitDB
from app.api.auth import router as auth_router

from app.api.subscription import router as subscription_router
from app.api.subscription_plan import router as subscription_plan_router
from app.api.visitor import router as visitor_router

app = FastAPI(
    title="Apartment Management API",
    description="REST API for Apartment Management System",
    version="1.0.0"
)



@app.on_event("startup")
def startup():
    InitDB.initialize()


# Authentication routes
app.include_router(auth_router)

app.include_router(subscription_router)

app.include_router(subscription_plan_router)

app.include_router(visitor_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Apartment Management API"
    }