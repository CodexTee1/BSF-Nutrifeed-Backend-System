# API Reference

Base URL: `http://127.0.0.1:5000`

## Public routes

### `GET /`
Returns a simple welcome payload.

Example response:
```json
{
  "message": "Welcome to the BSF-Nutrifeed backend",
  "health_check": "/health",
  "docs": "/docs"
}
```

### `GET /health`
Returns backend health status.

### `GET /docs`
Returns a lightweight JSON guide to the main endpoints.

## Authentication

### `POST /api/auth/register`
Registers an `admin` or `farmer`.

Admin example:
```json
{
  "full_name": "Admin User",
  "email": "admin@example.com",
  "password": "password123",
  "role": "admin"
}
```

Farmer example:
```json
{
  "full_name": "Farmer User",
  "email": "farmer@example.com",
  "password": "password123",
  "role": "farmer",
  "farm_id": 1
}
```

### `POST /api/auth/login`
Returns a JWT access token.

Example request:
```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

### `GET /api/auth/me`
Protected route. Returns current user details.

## Farms

### `POST /api/farms`
Protected route. Admin only.

Example request:
```json
{
  "name": "Main Farm",
  "location": "Lagos",
  "description": "Primary production site"
}
```

### `GET /api/farms`
Protected route. Lists farms.

## Users

### `GET /api/users`
Protected route. Admin only.

Optional query params:
- `role`
- `farm_id`
- `active`

## Feed Batches

### `POST /api/feed-batches`
Protected route. Admin only.

Example request:
```json
{
  "batch_code": "FB-001",
  "ingredient_source": "Palm kernel mix",
  "quantity_kg": 50,
  "production_date": "2026-03-27",
  "farm_id": 1
}
```

### `GET /api/feed-batches`
Protected route.

Optional query params:
- `page`
- `per_page`
- `status`
- `farm_id`

### `PATCH /api/feed-batches/<id>/status`
Protected route. Admin only.

Example request:
```json
{
  "status": "completed"
}
```

## Monitoring

### `POST /api/monitoring`
Protected route.

Example request:
```json
{
  "larvae_growth_mm": 12.5,
  "input_weight_kg": 20,
  "output_weight_kg": 15,
  "observation_date": "2026-03-27",
  "farm_id": 1,
  "feed_batch_id": 1
}
```

### `GET /api/monitoring`
Protected route.

Optional query params:
- `page`
- `per_page`
- `farm_id`
- `feed_batch_id`
- `observation_date`
