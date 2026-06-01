from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
import logging
from middleware import configure_middleware
from employees.router import router as employee_router
from auth.router import router as auth_router
from addresses.router import router as address_router
from departments.router import router as dept_router
from employee_departments.router import router as emp_dept_router
from exceptions.handlers import register_exception_handlers
from config import settings
# from config import APP_ENV
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(
    title="Employee App",
    description="Simple Employee App",
    version="1.0.0",
    # lifespan=lifespan,
)
configure_middleware(app)
register_exception_handlers(app)

app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(address_router)
app.include_router(dept_router)
app.include_router(emp_dept_router)


@app.get("/",tags=["Employee App"])
def root():
    return {"Welcome to employee app"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "env": settings.app_env}

# @app.exception_handler(NotFoundException)
# async def not_found_exception_handler(request:Request,exc:NotFoundException):
#     return JSONResponse(
#         status_code=404,
#         content={"detail":str(exc)}
#     )



# @dataclass
# class EmployeeCreate:
#     first_name: str
#     last_name: str
#     email: str


# class PublicPost(TypedDict):
#     id: int
#     first_name: str
#     last_name: str
#     email: str

#@app.get("/employee",status_code=200,response_model=PublicPost)
# def get_employee():
#     return _employees

# @app.post("/employee",status_code=201,response_model=PublicPost)
# def create_employee(emp:EmployeeCreate):
#     global _employees
#     global _emp_id
#     id = _emp_id
#     _employees[_emp_id]={
#         "id":id,
#         "first_name":emp.first_name,
#         "last_name":emp.last_name,
#         "email":emp.email
#     }
#     _emp_id+=1
#     return _employees[id]

# @app.get("/employee/{id}",status_code=200,response_model=PublicPost)
# def get_employee_byID(id):
#     return _employees[int(id)]

