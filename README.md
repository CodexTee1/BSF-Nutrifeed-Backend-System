# BSF-Nutrifeed Backend System

Backend system for the BSF-Nutrifeed platform, designed to support sustainable poultry feed production through secure data management, production tracking, and monitoring workflows.

## Features

- User management for admins and farmers
- Farm management
- Feed batch creation and tracking
- Monitoring record submission and retrieval
- JWT-based authentication and protected routes
- Docker support for containerized deployment

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- SQLite for local development

## Project Structure

- [`backend/`](./backend) contains the Flask application, routes, models, docs, and Docker setup
- [`tests/`](./tests) contains API test coverage

## Quick Start

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
flask --app run db init
flask --app run db migrate -m "Initial schema"
flask --app run db upgrade
python run.py
```

## Main Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/farms`
- `POST /api/feed-batches`
- `POST /api/monitoring`
- `GET /api/users`
- `GET /api/feed-batches`
- `GET /api/monitoring`

## Documentation

- Backend README: [`backend/README.md`](./backend/README.md)
- API reference: [`backend/docs/api_reference.md`](./backend/docs/api_reference.md)
- Debugging and performance report: [`backend/docs/debugging_performance_report.md`](./backend/docs/debugging_performance_report.md)
