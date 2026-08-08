from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    mobile: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8)
    apartment_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    mobile: str

class ForgotPasswordRequest(BaseModel):
    mobile: str = Field(
        ...,
        min_length=10,
        max_length=15,
    )

class VerifyOTPRequest(BaseModel):
    mobile: str = Field(
        ...,
        min_length=10,
        max_length=15,
    )

    otp: str = Field(
        ...,
        min_length=6,
        max_length=6,
    )

class ResetPasswordRequest(BaseModel):
    mobile: str = Field(
        ...,
        min_length=10,
        max_length=15,
    )

    new_password: str = Field(
        ...,
        min_length=8,
    )