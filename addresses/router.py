from sqlalchemy.ext.asyncio import AsyncSession
from addresses.schemas import AddressCreate, AddressResponse
import addresses.service as address_service
from fastapi import APIRouter, Depends, status
from database import get_db
from auth.dependencies import get_current_user


router = APIRouter(prefix="/addresses", tags=["Address"], dependencies=[Depends(get_current_user)])


@router.post("/employee/{emp_id}", response_model=AddressResponse)
async def create(emp_id: int, body: AddressCreate, db: AsyncSession = Depends(get_db)):
    address = await address_service.create(db, body, emp_id)
    return address


@router.get("", response_model=list[AddressResponse])
async def get_all_address(db: AsyncSession = Depends(get_db)):
    address = await address_service.get_all_address(db)
    return [add for add in address]


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address_byId(address_id: int, db: AsyncSession = Depends(get_db)):
    address = await address_service.get_address_byId(address_id, db)
    return address


@router.get("/employee/{emp_id}", response_model=list[AddressResponse])
async def get_address_by_empid(emp_id: int, db: AsyncSession = Depends(get_db)):
    address = await address_service.get_address_by_empid(emp_id, db)
    return address


@router.put("/{emp_id}/{address_id}", response_model=AddressResponse)
async def update_address(emp_id: int, address_id: int, body: AddressCreate, db: AsyncSession = Depends(get_db)):
    address = await address_service.update_address(emp_id, address_id, body, db)
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, db: AsyncSession = Depends(get_db)):
    await address_service.delete_address(address_id, db)
    return {f"Address with id {address_id} is deleted"}


@router.delete("/employee/{emp_id}/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_address(emp_id: int, address_id: int, db: AsyncSession = Depends(get_db)):
    await address_service.delete_employee_address(emp_id, address_id, db)
    return {"message": f"Address with id {address_id} of employee {emp_id} is deleted"}
