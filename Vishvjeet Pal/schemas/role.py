from pydantic import BaseModel
from typing import List
class RoleCreate(BaseModel):
    role: str
    permissions: List[str]

class RoleResponse(BaseModel):
    r_id: int
    role: str
    permissions: List[str]

    class Config:
        from_attributes = True
