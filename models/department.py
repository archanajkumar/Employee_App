from models.entity import Entity,datetime_to_iso
from typing import TYPE_CHECKING,Any
from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship
if TYPE_CHECKING:
    from models.employee_department import EmployeeDepartment
class Department(Entity):
    __abstract__ = False
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    employee_departments: Mapped[list["EmployeeDepartment"]]=relationship(
        "EmployeeDepartment", back_populates="department"
    )
    def to_api_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": datetime_to_iso(self.created_at),
            "updated_at": datetime_to_iso(self.updated_at),
            "deleted_at": datetime_to_iso(self.deleted_at),
        }