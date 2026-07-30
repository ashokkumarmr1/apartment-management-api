from fastapi import FastAPI
from app.core.init_db import create_database, create_tables

app = FastAPI(
    title="Apartment Management API",
    description="REST API for Apartment Management System",
    version="1.0.0"
)



@app.on_event("startup")
def startup():
    create_database()
    create_tables()

@app.get("/")
def root():
    return {
        "message": "Welcome to Apartment Management API"
    }