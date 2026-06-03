import pytest

from exceptions import NotFoundException
from departments import service as dept_service


@pytest.mark.asyncio
async def test_get_by_id_raises_for_unknown_id(db_session):

    with pytest.raises(NotFoundException) as exc_info:
        await dept_service.get_dept_byId(9999, db_session)

    assert "9999" in exc_info.value.detail
