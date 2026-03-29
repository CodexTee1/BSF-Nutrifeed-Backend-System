import pytest

from backend.app import create_app
from backend.app.extensions import db


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret"
    JWT_SECRET_KEY = "test-jwt-secret"
    JWT_ACCESS_TOKEN_EXPIRES = 3600


@pytest.fixture()
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register_user(client, role="admin", email="admin@example.com"):
    payload = {
        "full_name": "Test User",
        "email": email,
        "password": "password123",
        "role": role,
    }
    if role == "farmer":
        payload["farm_id"] = 1

    return client.post(
        "/api/auth/register",
        json=payload,
    )


def login_user(client, email="admin@example.com"):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": "password123"},
    )
    return response.get_json()["access_token"]


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_home_and_docs(client):
    home_response = client.get("/")
    docs_response = client.get("/docs")

    assert home_response.status_code == 200
    assert docs_response.status_code == 200


def test_register_and_login(client):
    register_response = register_user(client)
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.get_json()


def test_create_feed_batch_requires_admin(client):
    register_user(client)
    admin_token = login_user(client)
    client.post(
        "/api/farms",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Main Farm", "location": "Lagos"},
    )

    register_user(client, role="farmer", email="farmer@example.com")
    token = login_user(client, email="farmer@example.com")

    response = client.post(
        "/api/feed-batches",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "batch_code": "FB-001",
            "ingredient_source": "Palm kernel mix",
            "quantity_kg": 50,
            "production_date": "2026-03-25",
            "farm_id": 1,
        },
    )

    assert response.status_code == 403


def test_create_monitoring_record(client):
    register_user(client)
    admin_token = login_user(client)
    client.post(
        "/api/farms",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Main Farm", "location": "Lagos"},
    )

    register_user(client, role="farmer", email="farmer2@example.com")
    token = login_user(client, email="farmer2@example.com")

    response = client.post(
        "/api/monitoring",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "larvae_growth_mm": 12.5,
            "input_weight_kg": 20,
            "output_weight_kg": 15,
            "observation_date": "2026-03-25",
            "farm_id": 1,
        },
    )

    assert response.status_code == 201
