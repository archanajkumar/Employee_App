from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from models import Department, EmployeeDepartment, Employee
from exceptions import ConflictException
from sqlalchemy.orm import selectinload, with_loader_criteria


async def create(name: str, db: AsyncSession) -> Department:
    dept = Department(name=name)
    db.add(dept)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Department: {name} already exists")
    await db.refresh(dept)
    return dept


async def get_all_departments(db: AsyncSession) -> Department:
    stmt = select(Department).where(Department.deleted_at.is_(None))
    result = await db.scalars(stmt)
    dept = result.all()
    return dept


async def get_dept_byId(dept_id: int, db: AsyncSession) -> Department:
    stmt = select(Department).where(Department.id == dept_id, Department.deleted_at.is_(None))
    result = await db.scalars(stmt)
    dept = result.first()
    return dept


async def get_department_employees(dept_id: int, db: AsyncSession):
    stmt = (
        select(Department)
        .where(Department.id == dept_id, Department.deleted_at.is_(None))
        .options(
            selectinload(Department.employee_departments).selectinload(EmployeeDepartment.employee),
            with_loader_criteria(EmployeeDepartment, EmployeeDepartment.deleted_at.is_(None)),
            with_loader_criteria(Employee, Employee.deleted_at.is_(None)),
        )
    )
    result = await db.scalars(stmt)
    dept = result.all()
    return dept


async def update_department(dept: Department, name: str, db: AsyncSession) -> Department:
    dept.name = name
    db.add(dept)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Department {name} already exists")
    await db.refresh(dept)
    return dept


async def delete_department(dept: Department, db: AsyncSession) -> Department:
    dept.deleted_at = func.now()
    db.add(dept)
    await db.commit()
    await db.refresh(dept)
    return dept
