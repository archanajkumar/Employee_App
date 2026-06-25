"""
Employee entity — ORM mapped class for table `employees`.
"""

from typing import Any
from datetime import date

from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.entity import Entity, datetime_to_iso

# from models import Address
from typing import TYPE_CHECKING
import enum
from sqlalchemy import Enum


if TYPE_CHECKING:
    from models.address import Address
    from models.employee_department import EmployeeDepartment
    from models.employee_document import EmployeeDocument


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "Developer"
    HR = "HR"


class EmployeeStatus(str, enum.Enum):
    PROBATION = "Probation"
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    addresses: Mapped[list["Address"]] = relationship("Address", back_populates="employee")
    employee_departments: Mapped[list["EmployeeDepartment"]] = relationship(
        "EmployeeDepartment",
        back_populates="employee",
    )

    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(EmployeeStatus, name="employeestatus", values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable=False,
        server_default=EmployeeStatus.PROBATION.value,
    )

    role: Mapped[EmployeeRole] = mapped_column(
        Enum(EmployeeRole, name="employeerole", values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value,
    )
    experience: Mapped[int] = mapped_column(Integer, nullable=False)
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)

    document: Mapped["EmployeeDocument"] = relationship("EmployeeDocument", back_populates="employee", uselist=False)

    @property
    def departments(self):
        return [
            link.department
            for link in self.employee_departments
            if (link.deleted_at is None and link.department is not None and link.department.deleted_at is None)
        ]

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": datetime_to_iso(self.created_at),
            "updated_at": datetime_to_iso(self.updated_at),
            "deleted_at": datetime_to_iso(self.deleted_at),
            "addresses": [address.to_api_dict() for address in self.addresses if address.deleted_at is None],
            "departments": [
                employee_department.department.to_api_dict()
                for employee_department in self.employee_departments
                if (
                    employee_department.deleted_at is None
                    and employee_department.department is not None
                    and employee_department.department.deleted_at is None
                )
            ],
        }
