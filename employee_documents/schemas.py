from pydantic import BaseModel, ConfigDict


class EmployeeDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    file_name: str
    file_path: str
