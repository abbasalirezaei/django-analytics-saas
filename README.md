# Analytics Backend

A Django-based analytics backend service that provides website tracking and reporting capabilities.

## Features

- User authentication and authorization
- Website management
- Real-time analytics tracking
- Reporting and data visualization
- RESTful API endpoints

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (for caching and async tasks)
- Docker (optional, for containerized deployment)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd analytics-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Docker Setup

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

2. Run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Documentation

API documentation is available at `/api/docs/` when running the development server.

## Environment Variables

See `.env.example` for all available environment variables.

## Testing

Run the test suite with:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
