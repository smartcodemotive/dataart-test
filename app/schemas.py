from pydantic import BaseModel, EmailStr, Field


# --- User schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    limit: int
    offset: int


# --- Project schemas ---
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = ""
    owner_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

    model_config = {"from_attributes": True}
