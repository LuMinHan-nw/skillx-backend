from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.user_schema import UserResponse

ALLOWED_EMAIL_DOMAIN = "skillx.com"


# The upper limits match the column widths in app/models/user.py, so an
# oversized value is rejected as a validation error instead of reaching the
# database. The password cap is 72 because bcrypt ignores anything beyond that.
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=150)
    password: str = Field(..., min_length=6, max_length=72)
    phone: str | None = Field(default=None, max_length=20)

    @field_validator("email")
    @classmethod
    def email_must_be_skillx_domain(cls, value: str) -> str:
        if not value.lower().endswith(f"@{ALLOWED_EMAIL_DOMAIN}"):
            raise ValueError(f"Email must be a @{ALLOWED_EMAIL_DOMAIN} address")
        return value


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., max_length=150)
    password: str = Field(..., min_length=6, max_length=72)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
