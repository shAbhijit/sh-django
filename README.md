# SH Django Project

This is a Django-based project with Docker support for development and production environments.

## Features
- Django 3.2.x
- Django REST Framework 3.12.x
- Dockerized setup with `docker-compose`
- Development and production configurations

## Requirements
- Docker
- Docker Compose

## Setup
```bash
# Create Django App
docker-compose run --rm app sh -c "django-admin startproject app ."

# Run Tests
docker-compose run --rm app sh -c "python manage.py test"

# Run Linter
docker-compose run --rm app sh -c "flake8"

# TO create new module
docker-compose run --rm app sh -c "python manage.py startapp core"

# DB
docker-compose run --rm app sh -c "python manage.py wait_for_db"

# Migrations
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py migration"


# Run App
docker-compose up
```

### Development
1. Build and start the development environment:
   ```bash
   docker-compose up --build
   ```
2. Access the application at `http://localhost:8000`.

### Production
1. Update the `docker-compose.yml` file for production settings.
2. Build and start the production environment:
   ```bash
   docker-compose -f docker-compose.yml up --build
   ```

## License
This project is licensed under the MIT License.
