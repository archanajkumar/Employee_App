"""Employee Service"""

# import repositories.employee_repo as employee_repo
import employees.repo as employee_repo
from sqlalchemy.ext.asyncio import AsyncSession
from models import Employee
from exceptions import NotFoundException, BadRequestException
from auth.utils import hash_password
from addresses.schemas import AddressCreate
import addresses.repo as address_repo
from models.employee import EmployeeRole, EmployeeStatus
import employee_departments.service as emp_dept_service
from datetime import date

import logging

logger = logging.getLogger(__name__)


async def create(
    db: AsyncSession,
    name: str,
    email: str,
    age: int,
    password: str,
    address: AddressCreate,
    role: EmployeeRole,
    status: EmployeeStatus,
    experience: int,
    joining_date: date,
) -> Employee:
    hashed = hash_password(password)
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
        raise BadRequestException("email must be a non-empty string")
    employee = await employee_repo.create(
        db, name.strip(), email.strip(), age, role, status, experience, joining_date, password_hash=hashed
    )
    if address:
        address = await address_repo.create(db, address, employee.id)
    employee = await employee_repo.get_employee_ID(db, employee.id)
    return employee


async def get_employee(db: AsyncSession, status: EmployeeStatus | None = None) -> Employee:
    employee = await employee_repo.get_employee(db, status)
    return employee


async def get_employee_byname(db: AsyncSession, name: str):
    employee = await employee_repo.get_employee_byname(db, name)
    if not employee:
        # logger.warning(f"User: {name} not found")
        raise NotFoundException("Employee not found")
    return employee


async def get_employee_ID(db: AsyncSession, id: int) -> Employee:
    employee = await employee_repo.get_employee_ID(db, id)
    if not employee:
        raise NotFoundException(f"Employee with id {id} not found")
    return employee


async def update_employee(
    db: AsyncSession,
    id: int,
    name: str,
    email: str,
    age: int,
    status: EmployeeStatus,
    experience: int,
    joining_date: date,
) -> Employee:
    employee = await get_employee_ID(db, id)

    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
        raise BadRequestException("email must be a non-empty string")

    if employee.status == EmployeeStatus.PROBATION and status == EmployeeStatus.ACTIVE:
        today = date.today()

        months = (today.year - employee.joining_date.year) * 12 + (today.month - employee.joining_date.month)

        if today.day < employee.joining_date.day:
            months -= 1

        if months < 3:
            raise BadRequestException("Employee must complete at least 3 months of probation before becoming Active")
    updated_employee = await employee_repo.update_employee(
        db, employee, name, email, age, status, experience, joining_date
    )
    return updated_employee


async def delete_employee(db: AsyncSession, id: int) -> Employee:
    employee = await get_employee_ID(db, id)
    deleted_employee = await employee_repo.delete_employee(db, employee)
    await emp_dept_service.delete_by_empid(employee.id, db)
    return deleted_employee
