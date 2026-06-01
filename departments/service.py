from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException, NotFoundException
import departments.repo as dept_repo
from models import Department

async def create(name:str,db:AsyncSession) -> Department:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("Department name must be a non-empty string")
    dept = await dept_repo.create(name,db)
    return dept

async def get_all_departments(db:AsyncSession) -> Department:
    dept = await dept_repo.get_all_departments(db)
    return dept

async def get_dept_byId(dept_id:int, db:AsyncSession)->Department:
    dept = await dept_repo.get_dept_byId(dept_id,db)
    if not dept:
        raise NotFoundException(f"Department with id {dept_id} not found")
    return dept

async def update_department(dept_id:int, name:str, db:AsyncSession)->Department:
    dept = await get_dept_byId(dept_id, db)
    if not isinstance(name,str) or not name.strip():
        raise BadRequestException("Department name must be non-empty string")
    dept = await dept_repo.update_department(dept,name,db)
    return dept

async def delete_department(dept_id:int, db:AsyncSession)->Department:
    dept = await get_dept_byId(dept_id,db)
    dept = await dept_repo.delete_department(dept,db)
    return dept