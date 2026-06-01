from departments.schemas import DepartmentCreate, DepartmentResponse, DepartmentResponseById
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import departments.service as dept_service
from auth.dependencies import require_role
from models.employee import EmployeeRole


router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=DepartmentResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def create(body: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    dept = await dept_service.create(body.name, db)
    return dept


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[DepartmentResponse],
    dependencies=[Depends(require_role(EmployeeRole.HR, EmployeeRole.UI, EmployeeRole.UX, EmployeeRole.DEVELOPER))],
)
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    dept = await dept_service.get_all_departments(db)
    return dept


@router.get(
    "/{dept_id}",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentResponseById,
    dependencies=[Depends(require_role(EmployeeRole.HR, EmployeeRole.UI, EmployeeRole.UX, EmployeeRole.DEVELOPER))],
)
async def get_dept_byId(dept_id: int, db: AsyncSession = Depends(get_db)):
    dept = await dept_service.get_dept_byId(dept_id, db)
    return dept


@router.put("/{dept_id}", response_model=DepartmentResponseById, dependencies=[Depends(require_role(EmployeeRole.HR))])
async def update_department(dept_id: int, body: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    dept = await dept_service.update_department(dept_id, body.name, db)
    return dept


@router.delete(
    "/{dept_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(EmployeeRole.HR))]
)
async def delete_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    await dept_service.delete_department(dept_id, db)
    return {f"Department with id {dept_id} deleted"}
