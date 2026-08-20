from fastapi import APIRouter, Header, HTTPException, status


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

    return {
        "message": "You reached the protected profile",
        "token": token
    }