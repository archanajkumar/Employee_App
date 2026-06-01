from sqlalchemy.ext.asyncio import AsyncSession
from addresses.schemas import AddressCreate
import addresses.repo as address_repo
from models import Address
from fastapi import FastAPI,APIRouter,Depends
from  exceptions import NotFoundException, BadRequestException
import employees.service as emp_service

async def create(db:AsyncSession,body:AddressCreate,emp_id:int):
    if not isinstance(body.city, str) or not body.city.strip():
        raise BadRequestException("city must be a non-empty string")
    if not isinstance(body.line1, str) or not body.line1.strip():
        raise BadRequestException("line1 must be a non-empty string")
    if not isinstance(body.country, str) or not body.country.strip():
        raise BadRequestException("country must be a non-empty string")
    
    address = await address_repo.create(db,body,emp_id)
    return address

async def get_all_address(db:AsyncSession):
    address = await address_repo.get_all_address(db)
    return address

async def get_address_byId(address_id:int,db:AsyncSession):
    address = await address_repo.get_address_byId(address_id,db)
    if address is None:
        raise NotFoundException(f"Address with {address_id} not found")
    return address

async def get_address_by_empid(emp_id:int, db:AsyncSession):
    address = await address_repo.get_address_by_empid(emp_id,db)
    if address is None:
        raise NotFoundException(f"Address not found")
    return address

async def update_address(emp_id:int,address_id:int, body:AddressCreate, db:AsyncSession):
    address = await get_address_byId(address_id,db)
    address = await address_repo.update_address(emp_id,address,body,db)
    return address

async def delete_address(address_id:int, db:AsyncSession):
    address = await get_address_byId(address_id,db)
    address = await address_repo.delete_address(address,db)
    return address

async def delete_employee_address(emp_id:int, address_id:int, db:AsyncSession)->Address:
    emp = await emp_service.get_employee_ID(db,emp_id)
    address = await get_address_byId(address_id,db)
    if address.employee_id!=emp_id:
        raise BadRequestException(f"employee {emp_id} does not have address with id {address_id}")
    address = await address_repo.delete_address(address,db)
    return address
