# Django Analytics SaaS 🚀

A privacy-focused, high-performance analytics platform built with Django and Django REST Framework. Track pageviews, custom events, and user sessions with secure data isolation per organization.

![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-3.16-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Redis](https://img.shields.io/badge/Redis-7-red)
![Celery](https://img.shields.io/badge/Celery-5.3-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

## 🌟 Features

### 🔐 Authentication & Multi-tenancy
- **JWT Authentication** for dashboard access
- **API Key Authentication** for data collection
- **Role-based access control** (Admin, User, Viewer)
- **Complete data isolation** between organizations

### 📊 Analytics Tracking
- **Real-time pageview tracking**
- **Custom event tracking**
- **Session management** with enhanced lifecycle
- **Batch processing** for high-volume data
- **Advanced device & browser detection**

### 📈 Reporting & Analytics
- **Comprehensive dashboards** with real-time widgets
- **Time-series analytics** with multiple granularity
- **Top pages reports** with engagement metrics
- **Event analytics** with custom properties
- **Real-time visitor tracking** with geolocation

### ⚡ Performance
- **Redis caching** for frequent queries
- **Celery background tasks** for data processing
- **Database optimization** with proper indexing
- **API rate limiting** and request throttling

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 16.2
- Redis 6+
- Docker & Docker Compose (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/abbasalirezaei/django-analytics-saas.git
cd django-analytics-saas
```

2. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your database and Redis settings
```

3. **Run with Docker (Recommended)**
```bash
# Build and start all services
docker-compose up --build -d

# Run database migrations
docker-compose exec web python manage.py migrate

# Create a superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

The application will be available at `http://localhost:8000`

4. **Manual Installation (Development)**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
export DEBUG=True
export SECRET_KEY="your-secret-key"
export DB_NAME=analytics
export DB_USER=postgres
export DB_PASSWORD=password
export DB_HOST=localhost
export DB_PORT=5432
export REDIS_URL=redis://localhost:6379/0

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Start Celery worker (in separate terminal)
celery -A analytics_core worker --loglevel=info

# Start Celery beat (in separate terminal)
celery -A analytics_core beat --loglevel=info
```

## 🏗️ Project Structure

```
django-analytics-saas/
├── analytics_core/                 # Django project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── __init__.py
│   ├── celery.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                       # Authentication & user management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── organization.py
│   │   └── user.py
│   ├── api/v1/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── organization_service.py
│   │   └── user_service.py
│   ├── utils/
│   ├── migrations/
│   └── tests/
├── tracking/                       # Data collection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── website.py
│   │   ├── session.py
│   │   ├── pageview.py
│   │   └── event.py
│   ├── api/v1/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── tracking_service.py
│   │   ├── session_service.py
│   │   └── event_service.py
│   ├── utils/
│   ├── migrations/
│   └── tests/
├── reporting/                      # Analytics & reporting
│   ├── api/v1/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analytics_service.py
│   │   ├── aggregation_service.py
│   │   └── cache_service.py
│   ├── utils/
│   └── tests/
├── dashboard/                      # NEW: Dashboard app
│   ├── api/v1/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── services/
│   ├── static/
│   └── tests/
├── static/
│   └── tracking.js                # JavaScript tracking snippet
├── docker-compose.yml
├── docker-compose.prod.yml
├── requirements.txt
├── requirements-dev.txt
├── manage.py
└── README.md
```


```
django-analytics-saas/
├── analytics_core/                 # Django project settings
├── accounts/                       # Authentication & user management
├── tracking/                       # Data collection
├── reporting/                      # Analytics & reporting
├── dashboard/                      # Dashboard app
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

## 🔧 Configuration

### Environment Variables
```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DB_NAME=analytics
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific app tests
pytest accounts/tests/
pytest tracking/tests/
pytest reporting/tests/

# Run with coverage
pytest --cov=. --cov-report=html
```

## 🚀 Deployment

### Production Deployment
```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up --build -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## 🎯 Usage Examples

### Track Page View
```bash
curl -X POST http://localhost:8000/api/tracking/v1/pageview/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "domain": "example.com",
    "session_id": "user_session_123",
    "page_url": "/products/1",
    "page_title": "Product Page"
  }'
```

### Get Analytics
```bash
curl -X GET "http://localhost:8000/api/reporting/v1/overview/?days=7&website_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

> **API Documentation**: For complete API documentation, use Swagger UI at `/swagger/` or import `postman-api-docs.json` into Postman.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.