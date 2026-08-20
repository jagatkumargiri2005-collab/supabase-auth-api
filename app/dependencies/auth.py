from fastapi import Header, HTTPException, status
from supabase_auth.errors import AuthApiError

from app.supabase_client import supabase


def get_current_user(
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

        return {
            "user": response.user,
            "token": token
        }

    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )