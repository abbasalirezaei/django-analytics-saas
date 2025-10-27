# Analytics Backend - Simple Version

## 🚀 Quick Start

### 1. Start Docker Services
```bash
chmod +x restart-simple.sh
./restart-simple.sh
```

### 2. Access the Application
- **Main Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API Endpoints**:
  - Accounts: http://localhost:8000/api/accounts/
  - Tracking: http://localhost:8000/api/tracking/
  - Reporting: http://localhost:8000/api/reporting/

## 📋 API Endpoints

### Accounts API
- `POST /api/accounts/auth/register/` - Register new organization
- `POST /api/accounts/auth/login/` - Login
- `GET /api/accounts/organization/profile/` - Get organization profile
- `GET /api/accounts/user/profile/` - Get user profile

### Tracking API
- `POST /api/tracking/v1/pageview/` - Track page view
- `POST /api/tracking/v1/event/` - Track custom event
- `POST /api/tracking/v1/session/start/` - Start session
- `POST /api/tracking/v1/session/end/` - End session
- `POST /api/tracking/v1/batch/` - Batch tracking

### Reporting API
- `GET /api/reporting/api/v1/overview/` - Analytics overview
- `GET /api/reporting/api/v1/timeseries/` - Time series data
- `GET /api/reporting/api/v1/top-pages/` - Top pages
- `GET /api/reporting/api/v1/events/` - Event summary
- `GET /api/reporting/api/v1/realtime/` - Real-time stats
- `GET /api/reporting/api/v1/websites/` - Website list

## 🔧 Troubleshooting

### Redis Connection Issues
If you see Redis connection errors, make sure Redis is running:
```bash
docker-compose ps
```

### Database Issues
Run migrations manually:
```bash
docker-compose exec web python manage.py migrate
```

### Static Files (if needed later)
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## 📝 Notes

- This is a simplified version without Swagger documentation
- All API endpoints are functional
- Redis and PostgreSQL are included in Docker setup
- Celery workers are configured for background tasks
