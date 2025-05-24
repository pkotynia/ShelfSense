from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import RegisterRequest, AuthResponse, LoginRequest  # add missing import for login
from app.models import User
from app.dependencies import get_db
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse, status_code=201)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user. Returns user id, email, and JWT token.
    """
    # Check if email already exists
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    # Hash the password
    password_hash = auth_service.hash_password(data.password)
    # Create the user
    user = User(email=data.email, username=data.email, password_hash=password_hash)
    db.add(user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error during registration")
    db.refresh(user)
    # Generate JWT
    token = auth_service.create_access_token(user)
    return AuthResponse(id=user.id, email=user.email, token=token)

@router.post("/login", response_model=AuthResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
) -> AuthResponse:
    """Authenticate existing user and return JWT token"""
    return auth_service.authenticate(data, db)
