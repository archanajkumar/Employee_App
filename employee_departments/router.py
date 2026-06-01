from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
import employee_departments.service as emp_dept_service
from database import get_db
from auth.dependencies import require_role
from models.employee import EmployeeRole

router = APIRouter(prefix="/employee_department", tags=["Employee_Department"])


@router.post("/{emp_id}/departments/{dept_id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def attach(emp_id: int, dept_id: int, db: AsyncSession = Depends(get_db)):
    emp_dept = await emp_dept_service.attach(emp_id, dept_id, db)
    return emp_dept


@router.delete("/{emp_id}/departments/{dept_id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def dettach(emp_id: int, dept_id: int, db: AsyncSession = Depends(get_db)):
    await emp_dept_service.dettach(emp_id, dept_id, db)
    return {"message": "detached"}
