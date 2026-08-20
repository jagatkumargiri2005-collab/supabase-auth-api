from fastapi import APIRouter, Header, HTTPException, status
from app.supabase_client import supabase


router = APIRouter(
    tags=["Protected"]
)


@router.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


@router.get("/protected/profile")
def protected_profile(
    authorization: str | None = Header(default=None)
):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    token = authorization[7:]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    try:
        response = supabase.auth.get_user(token)

        user = response.user

        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )