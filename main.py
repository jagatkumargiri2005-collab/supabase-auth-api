from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.protected import router as protected_router


app = FastAPI(
    title="Authentication API",
    description="Authentication using Supabase",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Server running and connected to Supabase"
    }


app.include_router(auth_router)
app.include_router(protected_router)