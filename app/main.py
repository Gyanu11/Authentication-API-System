from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.database import Base, engine
from app.models.user import User



app = FastAPI(
    title="User Authentication and Management API",
    description="A practice project for learning backend development.",
    version="1.0.0",
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "User Authentication API is running"
    }

