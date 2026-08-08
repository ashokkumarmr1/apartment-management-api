from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# -----------------------------
# Login Request
# -----------------------------
class UserLogin(BaseModel):
    mobile: str
    password: str

# -----------------------------
# Register Request
# -----------------------------
class UserRegister(BaseModel):
    full_name: str
    mobile: str
    password: str
    gender: Optional[str] = None
    role_id: int
    apartment_id: int

# -----------------------------
# Update Request
# -----------------------------
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    mobile: Optional[str] = None
    gender: Optional[str] = None
    role_id: Optional[int] = None
    apartment_id: Optional[int] = None
    status: Optional[str] = None

# -----------------------------
# Response
# -----------------------------
class UserResponse(BaseModel):
    id: int
    full_name: str
    gender: Optional[str]
    role_id: int
    apartment_id: int
    status: str
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# -----------------------------
# Change Password Request
# -----------------------------

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# -----------------------------
# Common API Response
# -----------------------------
class ApiResponse(BaseModel):
    success: bool
    message: str


