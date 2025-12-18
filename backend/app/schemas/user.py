from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "employee"

class UserCreate(UserBase):
    password: str
    organization_name: str # For Phase 0 simple signup

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    organization_id: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass
