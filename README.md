# SH Django Project

This is a Django-based project with Docker support for development and production environments.

## Features
- Django 3.2.x
- Django REST Framework 3.12.x
- Dockerized setup with `docker-compose`
- Separate configurations for development and production

---

## Requirements
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Setup

### Create Django App
```bash
docker-compose run --rm app sh -c "django-admin startproject app ."
```

### Run Tests
```bash
docker-compose run --rm app sh -c "python manage.py test"
```

### Run Linter
```bash
docker-compose run --rm app sh -c "flake8"
```

### Create a New Module
```bash
docker-compose run --rm app sh -c "python manage.py startapp core"
docker-compose run --rm app sh -c "python manage.py startapp user"
docker-compose run --rm app sh -c "python manage.py startapp organizations"
```

### Database Commands
- **Wait for Database:**
  ```bash
  docker-compose run --rm app sh -c "python manage.py wait_for_db"
  ```

- **Make Migrations:**
  ```bash
  docker-compose run --rm app sh -c "python manage.py makemigrations"
  ```

- **Apply Migrations:**
  ```bash
  docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"
  ```

- **Update Migration:**
  ```bash
  docker-compose run --rm app sh -c "python manage.py migration"
  ```

### Create Superuser
```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

### Run the Application
```bash
docker-compose up
```

### Show URLS
```bash
docker-compose run --rm app sh -c "python manage.py show_urls"
```
---

## Development

1. Build and start the development environment:
   ```bash
   docker-compose up --build
   ```
2. Access the application at: [http://localhost:8000](http://localhost:8000)

---

## Production

1. Update the `docker-compose.yml` file for production settings.
2. Build and start the production environment:
   ```bash
   docker-compose -f docker-compose.yml up --build
   ```

---

## License
This project is licensed under the [MIT License](LICENSE).
