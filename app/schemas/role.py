from typing import Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleOut(RoleBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class RoleUpdate(RoleBase):
    name: Optional[str]
