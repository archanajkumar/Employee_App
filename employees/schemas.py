from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from addresses.schemas import AddressCreate, AddressResponse
from departments.schemas import DepartmentResponse
from models.employee import EmployeeRole, EmployeeStatus


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1)
    email: str
    age: int | None = Field(ge=0, le=150)
    address: AddressCreate | None = None
    password: str = Field(min_length=6)
    role: EmployeeRole
    status: EmployeeStatus
    experience: int | None = Field(ge=0)


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None = None
    role: EmployeeRole
    status: EmployeeStatus
    experience: int | None = None
    joining_date: date


class EmployeeResponseById(EmployeeResponse):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: datetime
    addresses: list[AddressResponse] = []
    departments: list[DepartmentResponse] = []


class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: str
    age: int | None = Field(ge=0, le=150)
    status: EmployeeStatus
