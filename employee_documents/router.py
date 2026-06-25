from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import employee_documents.service as document_service
from employee_documents.schemas import EmployeeDocumentResponse


router = APIRouter(prefix="/employee-documents", tags=["Employee Documents"])


@router.post("/{employee_id}", response_model=EmployeeDocumentResponse)
async def upload_document(employee_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    return await document_service.upload_document(db, employee_id, file)


@router.get("/employee/{employee_id}")
async def view_document(employee_id: int, db: AsyncSession = Depends(get_db)):
    document = await document_service.get_document_by_employee(db, employee_id)
    return {
        "id": document.id,
        "file_name": document.file_name,
        "file_path": document.file_path,
    }
