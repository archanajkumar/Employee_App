from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime
class DepartmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True,extra='forbid')

    name: str = Field(min_length=1)

class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class DepartmentResponseById(DepartmentResponse):
    created_at: datetime
    updated_at: datetime