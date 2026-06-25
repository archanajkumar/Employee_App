from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.employee_document import EmployeeDocument


async def create(
    db: AsyncSession,
    employee_id: int,
    file_name: str,
    file_path: str,
) -> EmployeeDocument:
    document = EmployeeDocument(
        employee_id=employee_id,
        file_name=file_name,
        file_path=file_path,
    )
    db.add(document)

    await db.commit()
    await db.refresh(document)

    return document


async def get_document_by_employee_Id(db: AsyncSession, employee_id: int):
    stmt = select(EmployeeDocument).where(
        EmployeeDocument.employee_id == employee_id, EmployeeDocument.deleted_at.is_(None)
    )
    result = await db.scalars(stmt)
    return result.first()


async def update_document(
    db,
    document: EmployeeDocument,
    file_name: str,
    file_path: str,
) -> EmployeeDocument:
    document.file_name = file_name
    document.file_path = file_path

    db.add(document)
    await db.commit()
    await db.refresh(document)

    return document
