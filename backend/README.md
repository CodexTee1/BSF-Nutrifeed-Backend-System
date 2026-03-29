# BSF-Nutrifeed Backend

Minimal Flask backend for:
- farmer and admin user management
- farm management
- feed batch records
- larvae growth and monitoring logs
- JWT-protected API access

## Quick start

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

## Docker

Build and run the backend with Docker:

```powershell
cd backend
docker build -t bsf-nutrifeed-backend .
docker run -p 5000:5000 --env-file .env bsf-nutrifeed-backend
```

## Local verification

Run this after installing dependencies to quickly verify the main flow.

From the project root:

```powershell
python -m backend.scripts.smoke_test
```

Or from inside `backend`:

```powershell
python scripts\smoke_test.py
```

Expected result: each listed endpoint should print a `200`, `201`, or other intentional success code.

## Core endpoints

- `GET /`
- `GET /health`
- `GET /docs`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/farms`
- `GET /api/farms`
- `GET /api/users`
- `POST /api/feed-batches`
- `GET /api/feed-batches`
- `PATCH /api/feed-batches/<id>/status`
- `POST /api/monitoring`
- `GET /api/monitoring`

## Example register payload

```json
{
  "full_name": "Ada Farmer",
  "email": "ada@example.com",
  "password": "securepass123",
  "role": "admin"
}
```

## Notes

- Create at least one farm before registering farmer accounts.
- Farmer registration now expects a `farm_id`.
- List endpoints support pagination with `page` and `per_page`.

## Simple demo order

1. Open `/` or `/docs` in the browser.
2. Register an admin account.
3. Log in and copy the JWT access token.
4. Create a farm with the admin token.
5. Register a farmer with the farm's `id`.
6. Create feed batches and monitoring records.

## Suggested manual endpoint test order

1. `GET /`
2. `GET /health`
3. `POST /api/auth/register` for admin.
4. `POST /api/auth/login` for admin
5. `POST /api/farms` with admin token
6. `POST /api/auth/register` for farmer with `farm_id`
7. `POST /api/feed-batches` with admin token
8. `POST /api/monitoring` with token
9. `GET /api/users`
10. `GET /api/feed-batches?page=1&per_page=5`
11. `GET /api/monitoring?page=1&per_page=5`

## Submission docs

- API reference: `docs/api_reference.md`
- Debugging/performance report: `docs/debugging_performance_report.md`
