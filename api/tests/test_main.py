import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import api.main as main_mod


@pytest.fixture(autouse=True)
def mock_redis():
    mock_instance = MagicMock()
    original = main_mod.r
    main_mod.r = mock_instance
    yield mock_instance
    main_mod.r = original


@pytest.fixture()
def client():
    return TestClient(main_mod.app)


def test_create_job_returns_job_id(client, mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36


def test_create_job_pushes_to_job_queue(client, mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1
    response = client.post("/jobs")
    job_id = response.json()["job_id"]
    mock_redis.lpush.assert_called_once_with("job", job_id)
    mock_redis.hset.assert_called_once_with(f"job:{job_id}", "status", "queued")


def test_get_job_returns_status(client, mock_redis):
    mock_redis.hget.return_value = "queued"
    response = client.get("/jobs/test-job-123")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "queued"


def test_get_job_not_found(client, mock_redis):
    mock_redis.hget.return_value = None
    response = client.get("/jobs/nonexistent-job")
    assert response.status_code == 404


def test_health_check_ok(client, mock_redis):
    mock_redis.ping.return_value = True
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_check_redis_down(client, mock_redis):
    import redis as redis_lib
    mock_redis.ping.side_effect = redis_lib.exceptions.ConnectionError("down")
    response = client.get("/health")
    assert response.status_code == 503
