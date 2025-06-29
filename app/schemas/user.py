from pydantic import BaseModel, EmailStr, computed_field, Field
from datetime import datetime
from typing import Optional

from app.models.role import Role


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role_id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None


from pydantic import BaseModel, EmailStr, computed_field
from datetime import datetime
from typing import Optional
from app.models.role import Role  # SQLAlchemy-модель


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    role_obj: Optional[Role] = Field(default=None, exclude=True)

    @computed_field
    @property
    def role(self) -> Optional[str]:
        return self.role_obj.name if self.role_obj else None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "arbitrary_types_allowed": True  # <-- обязательно при использовании ORM-объектов
    }



