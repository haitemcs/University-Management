# University Management System

A backend-first university management project built to practise relational database design and SQL, not only basic CRUD.

## Stack
- Python 3.12 and FastAPI
- PostgreSQL 16
- SQLAlchemy 2
- JWT access tokens
- Argon2 password hashing
- Pytest

## Main features
- Authentication: register, login, current user and JWT validation
- Role-based access: admin, teacher and student
- Academic data: departments, students, teachers, courses, enrollments and grades
- SQL reports: weighted student averages, course enrollment totals, department performance and top students
- Database features: foreign keys, unique/check constraints, indexes, views, PL/pgSQL functions and audit triggers

## Run with Docker
```bash
docker compose up --build
```
Then open http://localhost:8000/docs and test the API. Health check: http://localhost:8000/health.

The first database start runs SQL files from sql/. PostgreSQL only runs these scripts when its data volume is empty. To reset the demo database:
```bash
docker compose down -v
docker compose up --build
```
Warning: `docker compose down -v` deletes the database volume.

## Authentication
- `POST /auth/register` creates a student-role account.
- `POST /auth/login` returns a JWT.
- Click **Authorize** in Swagger and enter the token.
- `GET /auth/me` returns the authenticated user.
- Public registration cannot create admin or teacher accounts.

For a local demo, promote your registered account to admin directly in PostgreSQL:
```sql
UPDATE users
SET role_id = (SELECT id FROM roles WHERE name = 'admin')
WHERE email = 'your-email@example.com';
```

## Main endpoints
| Method | Endpoint | Access |
|---|---|---|
| POST | /auth/register | Public |
| POST | /auth/login | Public |
| GET | /auth/me | Authenticated |
| GET/POST | /departments | Public read; admin create |
| GET/POST | /students | Admin/teacher read; admin create |
| GET/POST | /courses | Public read; admin create |
| POST | /enrollments | Admin |
| POST | /grades | Admin/teacher |
| GET | /reports/student-gpa | Admin/teacher |
| GET | /reports/department-performance | Admin/teacher |
| GET | /reports/course-enrollment | Admin/teacher |
| GET | /reports/top-students | Admin/teacher |

## SQL learning path
1. `sql/01_schema.sql`: tables, primary keys, foreign keys, constraints and indexes.
2. `sql/02_analytics.sql`: views, PL/pgSQL functions and triggers.
3. `sql/03_practice_queries.sql`: joins, subqueries, NOT EXISTS, CASE, aggregation and window functions.

## Tests
Create a virtual environment, install requirements, configure `DATABASE_URL`, then run:
```bash
pytest
```

## Before production
This is an educational starter. Add Alembic migrations, refresh-token rotation, password reset, rate limiting, strict CORS settings, structured logging and more integration tests. Replace all demo secrets and passwords.
