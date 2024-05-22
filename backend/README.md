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

## Contributing

Thank you for your interest in contributing to our project! We welcome contributions from everyone and are grateful for every pull request.

### Prerequisites

- Python 3.7+
- Familiarity with Git

### Setting Up Your Development Environment

1. Fork the repository and clone your fork.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up local development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Coding Standards

Please follow the coding style and conventions established in the project. Use Black for Python.

### Submitting Changes

1. Create a new branch for your changes.
2. Make your changes and commit them with clear, concise commit messages.
3. Push your branch and submit a pull request to the main repository.
4. Await code review and address any feedback.

### Running Tests

Ensure that all tests pass before submitting a pull request. Add new tests for new features.

### Code Review Process

All submissions require review. We aim to review and respond to your pull request within 3 days.

### Community and Communication

Join our community on [Discord](#) for discussions and support.

