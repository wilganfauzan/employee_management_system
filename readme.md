# Employee Management System

A simple employee management system built with Django, featuring background task processing with Huey and Redis.

## Features

- Employee CRUD operations
- Department management
- Background tasks for report generation and notifications
- Export functionality
- Dashboard with statistics
- Dockerized deployment

## Tech Stack

- Django: Web framework
- PostgreSQL: Database
- Redis: Cache and task queue
- Huey: Task queue library
- Docker & Docker Compose: Containerization
- Bootstrap: Frontend styling

## Local Development Setup

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository
2. Create a `.env` file in the project root (see `.env.example` for required variables)
3. Start the containers:

```bash
docker-compose up -d
```

4. Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

5. Access the application at http://localhost:8000

## Background Tasks

The application uses Huey for background task processing. The following tasks are configured:

- Send welcome email to new employees
- Generate employee performance reports
- Daily department reports (runs at midnight)
- Weekly salary reports (runs every Monday at 9:00 AM)
- Export employee data to CSV

## VM Deployment

To deploy this application on a Virtual Machine:

1. Clone the repository on the VM:

```bash
git clone <repository-url>
cd employee_management_system
```

2. Create a `.env` file with production settings:

```
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://postgres:postgres@db:5432/employee_db
REDIS_URL=redis://redis:6379/0
```

3. Start the containers in detached mode:

```bash
docker-compose up -d
```

4. Run migrations and create a superuser:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

5. Set up a reverse proxy (like Nginx) to forward requests to the application.

## Production Considerations

For a production environment, consider the following:

1. Set up HTTPS using Let's Encrypt
2. Configure proper backups for PostgreSQL
3. Set up monitoring for containers
4. Configure email service for real email sending
5. Implement proper logging
6. Set up database replication or backup strategy

## License

MIT