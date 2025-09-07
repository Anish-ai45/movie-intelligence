from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.db import get_session

# Use in-memory SQLite for tests
engine = create_engine("sqlite://", connect_args={"check_same_thread": False})

def override_get_session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Override dependency
app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

def test_recent_starts_empty():
    resp = client.get("/recent")
    assert resp.status_code == 200
    assert resp.json() == []
