# """Employee Repo"""
# from fastapi import HTTPException,status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import IntegrityError
# from models import Employee
# from sqlalchemy import select,func


# async def create(db:AsyncSession, name:str, email:str)->Employee:
#     db_employee = Employee(name=name, email=email)
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee

# async def get_employee(db:AsyncSession)->Employee:
#     stmt = select(Employee).where(Employee.deleted_at.is_(None))
#     result = await db.scalars(stmt)
#     employee = result.all()
#     return employee

# async def get_employee_ID(db:AsyncSession,id:int)->Employee:
#     stmt = select(Employee).where(Employee.id==id,Employee.deleted_at.is_(None))
#     result = await db.scalars(stmt)
#     employee = result.first()
#     return employee

# async def update_employee(db:AsyncSession,employee:Employee,name:str,email:str)->Employee:
#     employee.name=name
#     employee.email=email

#     db.add(employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(employee)
#     return employee

# async def delete_employee(db:AsyncSession,employee:Employee)->Employee:
#     employee.deleted_at=func.now()
#     db.add(employee)
#     await db.commit()
#     await db.refresh(employee)
#     return employee
