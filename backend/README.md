# Backend for HAMS

## Technologies Used

- Python
- FastAPI
- SQLModel / SQLAlchemy

## Instructions

1. Create virtual environment

```shell
    python -m venv .venv
```

2. Activate enviroment

```shell
    # for macos and linux
    source .venv/bin/activate

    # for windows
    .venv\Scripts\activate
```

3. Install Dependencies

```shell
    pip install -r requirements.txt
```

4. Run the development server

```shell
    fastapi dev app.py
```

> Make sure to add a .env file with same as configuration as in .env.example

For the first time, make sure to apply database migrations:

```shell
    alembic revision --autogenerate -m "create database tables"
    alembic upgrade head 
```
