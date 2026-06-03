from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from models.employee import EmployeeRole


class DepartmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1)


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class DepartmentResponseById(DepartmentResponse):
    created_at: datetime
    updated_at: datetime


class EmployeeBasicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: EmployeeRole


class DepartmentEmployeeResponse(DepartmentResponse):
    employees: list[EmployeeBasicResponse] = []
