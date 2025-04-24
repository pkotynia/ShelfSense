from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date

# Authentication Schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    @validator('password')
    def password_complexity(cls, v: str) -> str:
        if not any(c.isalpha() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError('Password must contain both letters and numbers')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    id: UUID
    email: EmailStr
    token: str

    class Config:
        orm_mode = True

# User Schemas
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

    @validator('new_password')
    def new_password_complexity(cls, v: str) -> str:
        if not any(c.isalpha() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError('New password must contain both letters and numbers')
        return v

class MessageResponse(BaseModel):
    message: str

# Preferences Schemas
class PreferenceRequest(BaseModel):
    preferences_text: str = Field(..., min_length=1)

class PreferenceResponse(BaseModel):
    id: UUID
    preferences_text: str
    updated_at: datetime

    class Config:
        orm_mode = True

# Pagination Metadata
class PageMeta(BaseModel):
    total: int
    page: int
    limit: int

# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str]
    genre: Optional[str]
    description: Optional[str]
    publication_date: Optional[date]
    page_count: Optional[int]

    @validator('page_count')
    def non_negative_page_count(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError('page_count must be non-negative')
        return v

class BookCreateRequest(BookBase):
    pass

class BookUpdateRequest(BaseModel):
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    genre: Optional[str]
    description: Optional[str]
    publication_date: Optional[date]
    page_count: Optional[int]

    @validator('page_count')
    def non_negative_page_count(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError('page_count must be non-negative')
        return v

class BookResponse(BookBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BookListResponse(BaseModel):
    items: List[BookResponse]
    total: int
    page: int
    limit: int

# Library Entry Schemas
class LibraryEntryCreateRequest(BaseModel):
    book_id: UUID

class LibraryEntryResponse(BaseModel):
    id: UUID
    book_id: UUID
    created_at: datetime
    book: BookResponse

    class Config:
        orm_mode = True

class LibraryEntryListResponse(BaseModel):
    items: List[LibraryEntryResponse]
    total: int
    page: int
    limit: int

# Review Schemas
class ReviewRequest(BaseModel):
    review_text: str = Field(..., min_length=1)

class ReviewResponse(BaseModel):
    id: UUID
    review_text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Recommendation Schemas
class RecommendationResponse(BaseModel):
    id: UUID
    recommended_book: BookResponse
    created_at: datetime

    class Config:
        orm_mode = True

class RecommendationListResponse(BaseModel):
    items: List[RecommendationResponse]
    total: int
    page: int
    limit: int

# Rating Schemas
class RatingRequest(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)

    @validator('rating')
    def validate_rating_step(cls, v: float) -> float:
        if (v * 2) % 1 != 0:
            raise ValueError('Rating must be in increments of 0.5')
        return v

class RatingResponse(BaseModel):
    id: UUID
    rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# AI Review Template Schema
class AiReviewTemplateRequest(BaseModel):
    book_id: UUID
    notes: Optional[str]

class AiReviewTemplateResponse(BaseModel):
    template: str
