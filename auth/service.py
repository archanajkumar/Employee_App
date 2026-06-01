from auth.utils import verify_password,create_access_token,create_refresh_token,decode_access_token
import employees.repo as employee_repo
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import UnauthorizedException


async def login(db:AsyncSession, email:str,password:str):
    employee = await employee_repo.get_by_email(db,email)
    if employee is None:
        raise UnauthorizedException("invalid email or password")
    if not verify_password(password,employee.password_hash):
        raise UnauthorizedException("invalid email or password")

    # return create_access_token({"id":employee.id, "email":employee.email})
    access_token = create_access_token({"id":employee.id, "email":employee.email, "role":employee.role.value})
    refresh_token = create_refresh_token({"id":employee.id, "email":employee.email, "role":employee.role.value})
    return {"access_token":access_token, "refresh_token":refresh_token}

async def refresh(refresh_token:str):
    token = decode_access_token(refresh_token)
    if token is None:
        raise UnauthorizedException("invalid refresh token")
    if token.get("type")!="refresh":
        raise UnauthorizedException("invalid refreh token")
    access_token = create_access_token({"id":token["id"],"email":token["email"]})
    return access_token
