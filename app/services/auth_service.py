from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.models import User
from uuid import UUID
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas import LoginRequest, AuthResponse

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings (should be in config/env in production)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def hash_password(password: str) -> str:
    """Hash a password for storing in the database."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: User) -> str:
    """Generate a JWT token for the user."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def authenticate(request: LoginRequest, db: Session) -> AuthResponse:
    """Authenticate user credentials and return AuthResponse with JWT token."""
    # Fetch user by email
    user = db.query(User).filter(User.email == request.email).first()
    # If user not found or password invalid, raise 401
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Generate JWT token
    token = create_access_token(user)
    # Return response model
    return AuthResponse(id=user.id, email=user.email, token=token)
