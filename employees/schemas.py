from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from addresses.schemas import AddressCreate, AddressResponse
from departments.schemas import DepartmentResponse
from models.employee import EmployeeRole

# class AddressCreate(BaseModel):
#     line1: str
#     city: str
#     postal_code: str
#     country: str
#     @field_validator("postal_code")
#     @classmethod
#     def validate_postal_code(cls,v:str)->str:
#         if not v.isdigit():
#             raise ValueError("Postal code must contain only digits(0-9)")
#         return v

#     @model_validator(mode="after")

#     def postal_code_length_for_country(self):

#         country = self.country.strip().upper()

#         n = len(self.postal_code)

#         if country in ("US", "USA") and n != 5:

#             raise ValueError("US ZIP codes must be exactly 5 digits")

#         elif country == "IN" and n != 6:

#             raise ValueError("Indian PIN codes must be exactly 6 digits")

#         return self


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1)
    email: str
    age: int | None = Field(ge=0, le=150)
    address: AddressCreate | None = None
    password: str = Field(min_length=6)
    role: EmployeeRole


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None = None
    role: EmployeeRole


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
