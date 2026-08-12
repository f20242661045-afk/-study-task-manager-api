import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test_tasks.db"

    monkeypatch.setattr(
        "app.database.DATABASE_NAME",
        str(test_database),
    )

    from app.database import create_table

    create_table()

    with TestClient(app) as test_client:
        yield test_client