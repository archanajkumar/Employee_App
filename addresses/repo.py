from sqlalchemy.ext.asyncio import AsyncSession
from addresses.schemas import AddressCreate
from models import Address
from sqlalchemy import select, func


async def create(db: AsyncSession, body: AddressCreate, employee_id: int):
    address = Address(
        line1=body.line1, city=body.city, postal_code=body.postal_code, country=body.country, employee_id=employee_id
    )
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


async def get_all_address(db: AsyncSession):
    stmt = select(Address).where(Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    address = result.all()
    return address


async def get_address_byId(address_id: int, db: AsyncSession):
    stmt = select(Address).where(Address.id == address_id, Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    address = result.first()
    return address


async def get_address_by_empid(emp_id: int, db: AsyncSession):
    stmt = select(Address).where(Address.employee_id == emp_id, Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    address = result.all()
    return address


async def update_address(emp_id: int, address: Address, body: AddressCreate, db: AsyncSession):
    address.city = body.city
    address.country = body.country
    address.employee_id = emp_id
    address.line1 = body.line1
    address.postal_code = body.postal_code
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


async def delete_address(address: Address, db: AsyncSession):
    address.deleted_at = func.now()
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address
