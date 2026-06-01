from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import ConflictException,NotFoundException
import employee_departments.repo as emp_dept_repo
from models import EmployeeDepartment
import employees.service as emp_service
import departments.service as dept_service

async def attach(emp_id:int, dept_id:int, db:AsyncSession)-> EmployeeDepartment:
    await emp_service.get_employee_ID(db,emp_id)
    await dept_service.get_dept_byId(dept_id,db)
    result = await emp_dept_repo.get_records(emp_id,dept_id,db)
    if result:
        raise ConflictException("The record already exists, Department attached already")
    emp_dept = await emp_dept_repo.attach(emp_id,dept_id,db)
    return emp_dept

async def dettach(emp_id:int, dept_id:int, db: AsyncSession)->EmployeeDepartment:
    emp_dept = await emp_dept_repo.get_records(emp_id, dept_id, db)
    if not emp_dept:
        raise NotFoundException("employee-department record not found")
    emp_dept = await emp_dept_repo.dettach(emp_dept,db)
    return emp_dept