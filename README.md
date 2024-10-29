# Spy Cats Test Assignment

## Prerequisites
- Docker and Docker Compose
- Python 3.10 or higher


## Quick Start

### 1. Environment Setup
Create `.env` file from the example:
```bash
cp .env.example .env
```
Then configure enironment variables or leave them as default

### 2. Docker Containers
Start the PostgreSQL database and application server using Docker Compose:
```bash
docker compose up --build -d
```

### 3. Database Migrations
Execute the following commands to apply database migrations:
```bash
docker exec -i cats.api sh -c "alembic upgrade head"
```

### 4. Running the Application
The application should now be running at `http://0.0.0.0:8000`

## API Documentation
Once the server is running, you can access:
- Swagger UI documentation at `http://0.0.0.0:8000/docs`
- ReDoc documentation at `http://0.0.0.0:8000/redoc`

## Project Structure
```
src
    └── app
        ├── api
        │   ├── dependencies.py
        │   ├── root.py
        │   ├── routes
        │   │   ├── cats.py
        │   │   └── missions.py
        │   └── schemas
        │       ├── cats.py
        │       └── missions.py
        ├── db
        │   ├── migrations
        │   │   ├── env.py
        │   │   ├── README
        │   │   ├── script.py.mako
        │   │   └── versions
        │   │       └── 529f1a649945_init_tables.py
        │   ├── models
        │   │   ├── base.py
        │   │   ├── cats.py
        │   │   ├── missions.py
        │   │   └── targets.py
        │   ├── repositories
        │   │   ├── base.py
        │   │   ├── cat_repository.py
        │   │   └── mission_respository.py
        │   └── setup.py
        └── main
            ├── app.py
            └── config.py
```