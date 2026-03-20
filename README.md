# Enterprise AI Platform

🚀 **Enterprise-grade AI Platform** with microservices architecture, task queues, and ML model serving.

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   API Gateway   │────▶│  Auth Service   │────▶│   PostgreSQL    │
│    (FastAPI)    │     │   (JWT/OAuth)   │     │   (Users/Auth)  │
└────────┬────────┘     └─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ML Inference   │────▶│   Celery Worker │────▶│  Model Registry │
│    Service      │     │   (Task Queue)  │     │   (MinIO/S3)    │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│    Redis Cache  │     │  Message Queue  │
│   (Prediction   │     │    (RabbitMQ)   │
│     Cache)      │     │                 │
└─────────────────┘     └─────────────────┘
```

## 🌟 Features

- ✅ **FastAPI** - High-performance async API framework
- ✅ **JWT Authentication** - Secure token-based auth with refresh tokens
- ✅ **Celery + Redis** - Distributed task processing
- ✅ **ML Model Serving** - Load and serve TensorFlow/PyTorch models
- ✅ **Rate Limiting** - API throttling and abuse prevention
- ✅ **PostgreSQL** - Robust relational database with async support
- ✅ **Docker & Compose** - Full containerization
- ✅ **Monitoring** - Prometheus metrics and logging
- ✅ **Testing** - 90%+ code coverage with pytest
- ✅ **CI/CD** - GitHub Actions for automated testing and deployment

## 🚀 Quick Start

### Using Docker
```bash
# Clone repository
git clone https://github.com/efealtiparmakoglu/enterprise-ai-platform.git
cd enterprise-ai-platform

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec api alembic upgrade head

# Create superuser
docker-compose exec api python -m app.scripts.create_superuser
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up PostgreSQL and Redis
# Update .env file

# Run migrations
alembic upgrade head

# Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker (in another terminal)
celery -A app.celery_app worker --loglevel=info
```

## 📚 API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Authentication

```bash
# Get access token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secret"

# Use token
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🤖 ML Prediction API

```python
import requests

# Upload model
response = requests.post(
    "http://localhost:8000/api/v1/models/upload",
    headers={"Authorization": "Bearer TOKEN"},
    files={"model": open("model.pkl", "rb")}
)

# Make prediction
response = requests.post(
    "http://localhost:8000/api/v1/predict",
    headers={"Authorization": "Bearer TOKEN"},
    json={
        "model_id": "model-123",
        "input_data": {"features": [1.0, 2.0, 3.0]}
    }
)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_auth.py -v
```

## 📊 Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
- **Flower** (Celery): http://localhost:5555

## 🏢 Production Deployment

```bash
# Build production image
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/aiproduct

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

# Security
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ML Models
MODEL_STORAGE_PATH=/app/models
MAX_MODEL_SIZE_MB=500
```

## 👥 Authors

- **Efe Altıparmakoğlu** - [@efealtiparmakoglu](https://github.com/efealtiparmakoglu)

## 📄 License

MIT License - see [LICENSE](LICENSE) file
