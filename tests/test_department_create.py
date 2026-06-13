from departments import service as department_service
import pytest


@pytest.mark.asyncio
async def test_create_department_persists_name(db_session):

    fetched = await department_service.create("Engineering", db_session)

    assert fetched.id == 1
    assert fetched.name == "Engineering"
