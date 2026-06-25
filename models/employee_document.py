from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.employee import Employee


class EmployeeDocument(Entity):
    __abstract__ = False
    __tablename__ = "employee_documents"

    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    employee: Mapped["Employee"] = relationship("Employee", back_populates="document")
