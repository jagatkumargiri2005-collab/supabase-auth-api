import os

from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client

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