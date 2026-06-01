# """Employee Router"""
# from fastapi import HTTPException,status, Body, Depends,APIRouter
# from sqlalchemy.ext.asyncio import AsyncSession
# # from models import Employee
# from database import get_db
# import services.employee_service as employee_service


# router = APIRouter(prefix="/employee", tags=["Employees"])

# @router.post("", status_code=status.HTTP_201_CREATED)
# async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     name = body.get("name")
#     email = body.get("email")
#     employee = await employee_service.create(db,name,email)
#     return employee.to_api_dict()

# @router.get("")
# async def get_all_employees(db: AsyncSession = Depends(get_db)):
#     # breakpoint()
#     employee = await employee_service.get_employee(db)

#     for emp in employee:
#         print(emp.to_api_dict())
#     return [emp.to_api_dict() for emp in employee]
    
# @router.get("/{id}",status_code=status.HTTP_200_OK)
# async def get_employee_byID(id:int, db: AsyncSession = Depends(get_db)):
#     employee = await employee_service.get_employee_ID(db,id)
#     return employee.to_api_dict()

# @router.put("/{id}")
# async def update_employee(id:int, body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     name = body.get("name")
#     email = body.get("email")
#     employee = await employee_service.update_employee(db,id,name,email)
#     return employee.to_api_dict()

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_employee(id:int, db: AsyncSession = Depends(get_db)):
#     employee = await employee_service.delete_employee(db,id)
#     return {"message": "Employee deleted","details": employee.to_api_dict()}
    
