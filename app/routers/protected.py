from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user


router = APIRouter(
    tags=["Protected"]
)

@router.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }

@router.get("/protected/profile")
def protected_profile(current_user=Depends(get_current_user)):

    user = current_user["user"]
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

@router.get("/protected/dashboard")
def dashboard(current_user=Depends(get_current_user)):

    user = current_user["user"]
    return {
        "message": "Welcome to your dashboard",
        "user_id": user.id,
        "email": user.email
    }