"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column,relationship

from database import Base
from models.entity import Entity,datetime_to_iso
# from models import Employee
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.employee import Employee

class Address(Entity):
    __abstract__ = False
    __tablename__ = "address"

   
    line1: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str]=mapped_column(String(255),nullable=False)
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    employee: Mapped["Employee"] = relationship("Employee", back_populates="addresses")
    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "line1": self.line1,
            "city": self.city,
            "country":self.country,
            "created_at": datetime_to_iso(self.created_at),
            "updated_at": datetime_to_iso(self.updated_at),
            "deleted_at": datetime_to_iso(self.deleted_at),
        }