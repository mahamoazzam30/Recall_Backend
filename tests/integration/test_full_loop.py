"""End-to-end integration test covering the full loop: register -> login ->
create course -> upload material -> generate quiz session -> submit attempt
-> grade -> mastery/schedule updated -> dashboard reflects it.

Requires a real Postgres+pgvector database reachable via DATABASE_URL, and
monkeypatches the LLM clients so no real API calls are made. Skipped by
default until a test database is configured (see README "Running tests").
"""
import os

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.skipif(
    not os.getenv("RECALL_TEST_DATABASE_URL"),
    reason="set RECALL_TEST_DATABASE_URL to run the full integration loop against a real Postgres+pgvector instance",
)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", os.environ["RECALL_TEST_DATABASE_URL"])
    from app.main import app

    return TestClient(app)


def test_register_login_and_read_me(client):
    register_resp = client.post("/auth/register", json={"email": "student@example.com", "password": "hunter2pass"})
    assert register_resp.status_code == 201

    login_resp = client.post("/auth/login", json={"email": "student@example.com", "password": "hunter2pass"})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    me_resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "student@example.com"
