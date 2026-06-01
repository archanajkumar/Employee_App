"""Employee Repo"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models import Employee, Address, Department, EmployeeDepartment
from sqlalchemy import select, func, update
from exceptions import ConflictException
from sqlalchemy.orm import selectinload, with_loader_criteria
from models.employee import EmployeeRole


async def create(db: AsyncSession, name: str, email: str, age: int, role: EmployeeRole, password_hash: str) -> Employee:
    db_employee = Employee(name=name, email=email, age=age, role=role, password_hash=password_hash)
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email.strip()}' is already in use")
    await db.refresh(db_employee)
    return db_employee


async def get_employee(db: AsyncSession) -> Employee:
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    employee = result.all()
    return employee


async def get_employee_byname(db: AsyncSession, name: str) -> Employee:
    stmt = (
        select(Employee)
        .where(Employee.name.ilike(name), Employee.deleted_at.is_(None))
        .options(
            selectinload(Employee.addresses),
            selectinload(Employee.employee_departments).selectinload(EmployeeDepartment.department),
            with_loader_criteria(Address, Address.deleted_at.is_(None)),
            with_loader_criteria(EmployeeDepartment, EmployeeDepartment.deleted_at.is_(None)),
            with_loader_criteria(Department, Department.deleted_at.is_(None)),
        )
    )
    result = await db.scalars(stmt)
    employee = result.first()
    return employee


async def get_by_email(db: AsyncSession, email: str) -> Employee | None:
    stmt = select(Employee).where(Employee.email.ilike(email), Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    employee = result.first()
    return employee


async def get_employee_ID(db: AsyncSession, id: int) -> Employee:
    # stmt = select(Employee).where(Employee.id==id,Employee.deleted_at.is_(None)).options(
    #         selectinload(Employee.addresses),
    #         selectinload(Employee.departments),
    #         with_loader_criteria(
    #             Address,
    #             Address.deleted_at.is_(None)
    #         ),
    #         with_loader_criteria(
    #             Department,
    #             Department.deleted_at.is_(None)
    #         )
    #     )
    stmt = (
        select(Employee)
        .where(Employee.id == id, Employee.deleted_at.is_(None))
        .options(
            selectinload(Employee.addresses),
            selectinload(Employee.employee_departments).selectinload(EmployeeDepartment.department),
            with_loader_criteria(Address, Address.deleted_at.is_(None)),
            with_loader_criteria(EmployeeDepartment, EmployeeDepartment.deleted_at.is_(None)),
            with_loader_criteria(Department, Department.deleted_at.is_(None)),
        )
    )
    result = await db.scalars(stmt)
    employee = result.first()
    return employee


# async def get_employee_ID(db:AsyncSession,id:int)->Employee:
#     stmt = select(Employee).where(Employee.id==id,Employee.deleted_at.is_(None))
#     result = await db.scalars(stmt)
#     employee = result.first()
#     return employee


async def update_employee(db: AsyncSession, employee: Employee, name: str, email: str, age: int) -> Employee:
    employee.name = name
    employee.email = email
    employee.age = age

    db.add(employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email.strip()}' is already in use")
    await db.refresh(employee)
    return employee


# async def update_employee(db:AsyncSession,employee:Employee,name:str,email:str)->Employee:
#     employee.name=name
#     employee.email=email

#     db.add(employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise ConflictException(f"Email '{email.strip()}' is already in use")
#     await db.refresh(employee)
#     return employee


async def delete_employee(db: AsyncSession, employee: Employee) -> Employee:
    employee.deleted_at = func.now()
    db.add(employee)

    await db.execute(update(Address).where(Address.employee_id == employee.id).values(deleted_at=func.now()))
    await db.commit()
    await db.refresh(employee)
    return employee

    # await db.commit()
    # await db.refresh(employee)

    # stmt = select(Address).where(Address.employee_id==employee.id)
    # result = await db.scalars(stmt)
    # address = result.all()
    # for add in address:
    #     add.deleted_at=func.now()
    # db.add(address)
    # await db.commit()
    # await db.refresh(address)
    # return employee
