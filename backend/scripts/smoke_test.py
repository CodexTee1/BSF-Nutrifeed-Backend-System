from pathlib import Path
import sys


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_BACKEND_DIR = CURRENT_DIR.parent
PROJECT_ROOT_DIR = PROJECT_BACKEND_DIR.parent

for path in (PROJECT_BACKEND_DIR, PROJECT_ROOT_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

try:
    from backend.app import create_app
    from backend.app.extensions import db
except ModuleNotFoundError:
    from app import create_app
    from app.extensions import db


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret"
    JWT_SECRET_KEY = "test-jwt-secret"
    JWT_ACCESS_TOKEN_EXPIRES = 3600


def run_smoke_test():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        client = app.test_client()

        responses = []

        responses.append(("GET /", client.get("/").status_code))
        responses.append(("GET /health", client.get("/health").status_code))
        responses.append(("GET /docs", client.get("/docs").status_code))

        admin_register = client.post(
            "/api/auth/register",
            json={
                "full_name": "Admin User",
                "email": "admin@example.com",
                "password": "password123",
                "role": "admin",
            },
        )
        responses.append(("POST /api/auth/register admin", admin_register.status_code))

        admin_login = client.post(
            "/api/auth/login",
            json={"email": "admin@example.com", "password": "password123"},
        )
        responses.append(("POST /api/auth/login admin", admin_login.status_code))
        token = admin_login.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        farm_create = client.post(
            "/api/farms",
            headers=headers,
            json={"name": "Main Farm", "location": "Lagos"},
        )
        responses.append(("POST /api/farms", farm_create.status_code))

        farmer_register = client.post(
            "/api/auth/register",
            json={
                "full_name": "Farmer User",
                "email": "farmer@example.com",
                "password": "password123",
                "role": "farmer",
                "farm_id": 1,
            },
        )
        responses.append(("POST /api/auth/register farmer", farmer_register.status_code))

        feed_batch_create = client.post(
            "/api/feed-batches",
            headers=headers,
            json={
                "batch_code": "FB-001",
                "ingredient_source": "Palm kernel mix",
                "quantity_kg": 50,
                "production_date": "2026-03-26",
                "farm_id": 1,
            },
        )
        responses.append(("POST /api/feed-batches", feed_batch_create.status_code))

        monitoring_create = client.post(
            "/api/monitoring",
            headers=headers,
            json={
                "larvae_growth_mm": 12.5,
                "input_weight_kg": 20,
                "output_weight_kg": 15,
                "observation_date": "2026-03-26",
                "farm_id": 1,
                "feed_batch_id": 1,
            },
        )
        responses.append(("POST /api/monitoring", monitoring_create.status_code))

        responses.append(("GET /api/users", client.get("/api/users", headers=headers).status_code))
        responses.append(
            ("GET /api/feed-batches", client.get("/api/feed-batches?page=1&per_page=5", headers=headers).status_code)
        )
        responses.append(
            ("GET /api/monitoring", client.get("/api/monitoring?page=1&per_page=5", headers=headers).status_code)
        )

        for name, status_code in responses:
            print(f"{name}: {status_code}")


if __name__ == "__main__":
    run_smoke_test()
