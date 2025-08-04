# Django Shop - Docker Setup for Local Development

This Django project is configured to run with Docker and Docker Compose on local Linux systems.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### Development Environment

1. Clone the repository and navigate to the project directory:
   ```bash
   cd djangoshop
   ```

2. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

3. Build and run the development environment:
   ```bash
   docker-compose up --build
   ```

4. The application will be available at `http://localhost:8000`

### Production Environment (Local)

1. Use the production docker-compose file:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

2. The application will be available at `http://localhost:8000`

## Docker Commands

### Development

- **Start services**: `docker-compose up`
- **Start services in background**: `docker-compose up -d`
- **Build and start**: `docker-compose up --build`
- **Stop services**: `docker-compose down`
- **View logs**: `docker-compose logs`
- **Run Django commands**: `docker-compose exec web python manage.py <command>`

### Production

- **Start production services**: `docker-compose -f docker-compose.prod.yml up -d`
- **Stop production services**: `docker-compose -f docker-compose.prod.yml down`
- **View production logs**: `docker-compose -f docker-compose.prod.yml logs`

## Useful Django Commands in Docker

```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic

# Run tests
docker-compose exec web python manage.py test

# Django shell
docker-compose exec web python manage.py shell
```

## Environment Variables

The following environment variables can be configured in your `.env` file:

- `DEBUG`: Set to 0 for production, 1 for development
- `SECRET_KEY`: Django secret key
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection URL

## Services

### Development (`docker-compose.yml`)
- **web**: Django application running with development server
- **db**: PostgreSQL database

### Production (`docker-compose.prod.yml`)
- **web**: Django application running with Gunicorn
- **db**: PostgreSQL database

## Database

The project is configured to use PostgreSQL in Docker, but will fall back to SQLite if no `DATABASE_URL` environment variable is provided.

## Static Files

Static files are served by Django in both development and production modes. In production, they are collected using `collectstatic`.

## Volumes

- `postgres_data`: Persistent PostgreSQL data

## Ports

- **Django Application**: 8000
- **PostgreSQL**: 5432

## Local Development Without Docker

If you prefer to run without Docker:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file and run migrations:
   ```bash
   cp .env.example .env
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```
