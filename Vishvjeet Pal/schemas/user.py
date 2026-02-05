from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    r_id: int
    team: str
    email: EmailStr
    mobile: str
    password: str

class UserResponse(BaseModel):
    e_id: int
    name: str
    team: str
    email: EmailStr
    mobile: str
    r_id: int

    class Config:
        from_attributes = True
