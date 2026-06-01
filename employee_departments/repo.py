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
