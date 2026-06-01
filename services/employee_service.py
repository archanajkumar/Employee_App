# """Employee Service"""
# import repositories.employee_repo as employee_repo
# from fastapi import HTTPException,status
# from sqlalchemy.ext.asyncio import AsyncSession
# from models import Employee

# async def create(db: AsyncSession, name: str, email: str) -> Employee:
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#     employee = await employee_repo.create(db, name.strip(), email.strip())
#     return employee

# async def get_employee(db:AsyncSession)->Employee:
#     employee = await employee_repo.get_employee(db)
#     return employee

# async def get_employee_ID(db:AsyncSession,id:int)->Employee:
#     employee = await employee_repo.get_employee_ID(db,id)
#     if not employee:
#         raise HTTPException(404, "Employee not found")
#     return employee

# async def update_employee(db:AsyncSession,id:int, name:str,email:str)->Employee:
#     employee = await employee_repo.get_employee_ID(db,id)

#     if not employee:
#         raise HTTPException(404, "Employee not found")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
    
#     updated_employee = await employee_repo.update_employee(db,employee,name.strip(),email.strip())
#     return updated_employee

# async def delete_employee(db:AsyncSession,id:int)->Employee:
#     employee = await employee_repo.get_employee_ID(db,id)
    
#     if not employee:
#         raise HTTPException(404, "Employee not found")
#     deleted_employee = await employee_repo.delete_employee(db,employee)
#     return deleted_employee