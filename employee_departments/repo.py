from sqlalchemy.ext.asyncio import AsyncSession
from models import EmployeeDepartment
from sqlalchemy import select, func


async def get_records(emp_id: int, dept_id: int, db: AsyncSession) -> EmployeeDepartment:
    stmt = select(EmployeeDepartment).where(
        EmployeeDepartment.employee_id == emp_id,
        EmployeeDepartment.department_id == dept_id,
        EmployeeDepartment.deleted_at.is_(None),
    )
    result = await db.scalars(stmt)
    emp_dept = result.first()
    return emp_dept


async def attach(emp_id: int, dept_id: int, db: AsyncSession) -> EmployeeDepartment:
    emp_dept = EmployeeDepartment(employee_id=emp_id, department_id=dept_id)
    db.add(emp_dept)
    await db.commit()
    await db.refresh(emp_dept)
    return emp_dept


async def dettach(emp_dept: EmployeeDepartment, db: AsyncSession) -> EmployeeDepartment:
    emp_dept.deleted_at = func.now()
    db.add(emp_dept)
    await db.commit()
    await db.refresh(emp_dept)
    return emp_dept


async def get_by_empid(emp_id: int, db: AsyncSession) -> EmployeeDepartment:
    stmt = select(EmployeeDepartment).where(
        EmployeeDepartment.employee_id == emp_id, EmployeeDepartment.deleted_at.is_(None)
    )
    result = await db.scalars(stmt)
    emp_dept = result.all()
    return emp_dept


async def get_by_did(dept_id: int, db: AsyncSession) -> EmployeeDepartment:
    stmt = select(EmployeeDepartment).where(
        EmployeeDepartment.department_id == dept_id, EmployeeDepartment.deleted_at.is_(None)
    )
    result = await db.scalars(stmt)
    emp_dept = result.all()
    return emp_dept


async def delete_by_empid(emp_dept: list[EmployeeDepartment], db: AsyncSession) -> EmployeeDepartment:
    for emp in emp_dept:
        emp.deleted_at = func.now()
        db.add(emp)
    await db.commit()
    for emp in emp_dept:
        await db.refresh(emp)

    return emp_dept


async def delete_by_did(emp_dept: list[EmployeeDepartment], db: AsyncSession) -> EmployeeDepartment:
    for emp in emp_dept:
        emp.deleted_at = func.now()
        db.add(emp)
    await db.commit()
    for emp in emp_dept:
        await db.refresh(emp)

    return emp_dept
