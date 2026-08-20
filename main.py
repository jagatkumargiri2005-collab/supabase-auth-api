import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from supabase import Client, create_client
from supabase_auth.errors import AuthApiError
from app.schemas.auth import AuthRequest
from fastapi import Header

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

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


@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(request: AuthRequest):

    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })

        return {
            "user": response.user
        }

    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/auth/login")
def login(request: AuthRequest):

    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials"
        )

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }

@app.get("/protected/profile")
def protected_profile(authorization: str | None = Header(default=None)):

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

    return {
        "message": "You reached the protected profile",
        "token": token
    }