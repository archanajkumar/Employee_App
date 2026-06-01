from departments.schemas import DepartmentCreate,DepartmentResponse,DepartmentResponseById
from fastapi import APIRouter,Body,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import departments.service as dept_service
from auth.dependencies import get_current_user


router = APIRouter(prefix="/departments",tags=["Departments"],dependencies=[Depends(get_current_user)])

@router.post("",status_code=status.HTTP_201_CREATED,response_model=DepartmentResponse)
async def create(body:DepartmentCreate,db:AsyncSession=Depends(get_db)):
    dept = await dept_service.create(body.name,db)
    return dept

@router.get("",status_code=status.HTTP_200_OK,response_model=list[DepartmentResponse])
async def get_all_departments(db:AsyncSession=Depends(get_db)):
    dept = await dept_service.get_all_departments(db)
    return dept

@router.get("/{dept_id}",status_code=status.HTTP_200_OK,response_model=DepartmentResponseById)
async def get_dept_byId(dept_id:int, db:AsyncSession=Depends(get_db)):
    dept = await dept_service.get_dept_byId(dept_id,db)
    return dept

@router.put("/{dept_id}",response_model=DepartmentResponseById)
async def update_department(dept_id:int, body:DepartmentCreate, db:AsyncSession=Depends(get_db)):
    dept = await dept_service.update_department(dept_id,body.name,db)
    return dept

@router.delete("/{dept_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(dept_id:int, db:AsyncSession=Depends(get_db)):
    dept = await dept_service.delete_department(dept_id,db)
    return {f"Department with id {dept_id} deleted"}