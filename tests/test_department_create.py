# tests/test_employee_service.py

# `pytest_asyncio` provides the *async-aware* fixture decorator. Plain
# `@pytest.fixture` doesn't know how to drive an `async def` body — you
# have to use `@pytest_asyncio.fixture` whenever the fixture itself is
# async or yields an async resource.
# Same async-flavoured SQLAlchemy imports as the previous slide.

from departments import service as department_service
import pytest
# The fixture: a single function that owns the engine, the schema, and
# the session — and tears it all back down when the test finishes.


# The test is now pure "act + assert" — no engine, no create_all, no
# cleanup. Pytest sees the `db_session` parameter, runs the fixture
# above, and hands the yielded session in.
@pytest.mark.asyncio
async def test_create_department_persists_name(db_session):

    fetched = await department_service.create("Engineering", db_session)

    assert fetched.id == 1
    assert fetched.name == "Engineering"
