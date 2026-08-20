from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase_auth.errors import AuthApiError
from app.supabase_client import supabase


security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
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