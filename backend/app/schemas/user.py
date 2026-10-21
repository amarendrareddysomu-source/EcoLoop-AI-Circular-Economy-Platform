from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    location: Optional[str] = "Local City"

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    role: Optional[str] = "user"
    organization_id: Optional[int] = None
    organization_name: Optional[str] = None
    organization_type: Optional[str] = None # ngo or recycling_center

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    location: Optional[str] = None
    role: Optional[str] = None
    organization_id: Optional[int] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Alias for Module 3 spec
LoginRequest = UserLogin

class RefreshTokenInput(BaseModel):
    refresh_token: str

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    role: str
    organization_id: Optional[int] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: UserResponse

# Alias for Module 3 spec
TokenResponse = Token
