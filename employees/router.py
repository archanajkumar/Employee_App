"""Employee Router"""

from fastapi import status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

# from models import Employee
from database import get_db

# import services.employee_service as employee_service
import employees.service as employee_service
from employees.schemas import EmployeeCreate, EmployeeResponse, EmployeeResponseById, EmployeeUpdate
from auth.dependencies import require_role
from models.employee import EmployeeRole, EmployeeStatus
import logging

logger = logging.getLogger(__name__)

# router = APIRouter(prefix="/employee", tags=["Employees"],dependencies=[Depends(get_current_user)])
router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeResponseById,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def create_employee(body: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    name = body.name
    email = body.email
    age = body.age
    password = body.password
    address = body.address
    role = body.role
    status = body.status
    experience = body.experience
    joining_date = body.joining_date
    employee = await employee_service.create(
        db, name, email, age, password, address, role, status, experience, joining_date
    )
    return employee


# @router.get("",response_model=list[EmployeeResponse])
# async def get_all_employees(db: AsyncSession = Depends(get_db),_current_user:TokenPayload=Depends(get_current_user,)):
#     # breakpoint()
#     employee = await employee_service.get_employee(db)
#     return [emp for emp in employee]


@router.get(
    "",
    response_model=list[EmployeeResponse],
    dependencies=[Depends(require_role(EmployeeRole.HR, EmployeeRole.UI, EmployeeRole.UX, EmployeeRole.DEVELOPER))],
)
async def get_all_employees(status: EmployeeStatus | None = None, db: AsyncSession = Depends(get_db)):
    # breakpoint()
    employee = await employee_service.get_employee(db, status)
    return [emp for emp in employee]


@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeResponseById,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def get_employee_byname(name: str, db: AsyncSession = Depends(get_db)):
    employee = await employee_service.get_employee_byname(db, name)
    return employee


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeResponseById,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def get_employee_byID(id: int, db: AsyncSession = Depends(get_db)):
    employee = await employee_service.get_employee_ID(db, id)
    return employee


@router.put("/{id}", response_model=EmployeeResponse, dependencies=[Depends(require_role(EmployeeRole.HR))])
async def update_employee(id: int, body: EmployeeUpdate, db: AsyncSession = Depends(get_db)):
    name = body.name
    email = body.email
    age = body.age
    status = body.status
    experience = body.experience
    joining_date = body.joining_date
    employee = await employee_service.update_employee(db, id, name, email, age, status, experience, joining_date)
    return employee


@router.delete("/{id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def delete_employee(id: int, db: AsyncSession = Depends(get_db)):
    await employee_service.delete_employee(db, id)
    return {"message": "Employee deleted"}
