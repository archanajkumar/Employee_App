import os

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

import employee_documents.repo as document_repo
import employees.service as employee_service
from exceptions import NotFoundException

UPLOAD_DIR = "uploads"


async def upload_document(
    db: AsyncSession,
    employee_id: int,
    file: UploadFile,
):
    print("Filename:", file.filename)
    content = await file.read()
    print("Size:", len(content))

    employee = await employee_service.get_employee_ID(db, employee_id)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = f"{UPLOAD_DIR}/{employee_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    existing_document = await document_repo.get_document_by_employee_Id(
        db,
        employee_id,
    )

    if existing_document:
        # delete old physical file
        if os.path.exists(existing_document.file_path):
            os.remove(existing_document.file_path)

        return await document_repo.update_document(
            db,
            existing_document,
            file.filename,
            file_path,
        )

    print("Saved:", os.path.abspath(file_path))
    document = await document_repo.create(
        db,
        employee.id,
        file.filename,
        file_path,
    )
    return document


async def get_document_by_employee(db: AsyncSession, employee_id: int):
    document = await document_repo.get_document_by_employee_Id(db, employee_id)
    if not document:
        raise NotFoundException("Document not found")
    return document
