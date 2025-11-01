# Deployment Guide

This guide covers deployment options for the HTW Emerging Photo anonymization system.

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 10GB+ disk space

### Quick Deploy

```bash
# Clone repository
git clone <repository-url>
cd htw-emerging-photo

# Deploy with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Access Points
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Configuration

Edit `docker-compose.yml` to customize:

```yaml
environment:
  - MAX_UPLOAD_SIZE=10485760          # 10MB
  - FACE_CONFIDENCE_THRESHOLD=0.7     # 0.0-1.0
  - PLATE_CONFIDENCE_THRESHOLD=0.6    # 0.0-1.0
  - ANONYMIZATION_COLOR=#FFFF00       # Hex color
  - LOG_LEVEL=INFO                    # DEBUG/INFO/WARNING/ERROR
```

### Scaling

```bash
# Scale backend instances
docker-compose up -d --scale backend=3

# Note: Frontend should remain at 1 instance
```

### Stopping

```bash
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🖥️ Local Development Deployment

### Prerequisites
- Python 3.10+
- pip
- 4GB+ RAM

### Setup

```bash
# Clone repository
git clone <repository-url>
cd htw-emerging-photo

# Run setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Activate environment
source venv/bin/activate
```

### Running

**Terminal 1 - Backend**:
```bash
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend**:
```bash
source venv/bin/activate
streamlit run frontend/app.py
```

### Configuration

Edit `.env` file:
```bash
API_HOST=0.0.0.0
API_PORT=8000
MAX_UPLOAD_SIZE=10485760
FACE_CONFIDENCE_THRESHOLD=0.7
PLATE_CONFIDENCE_THRESHOLD=0.6
ANONYMIZATION_COLOR=#FFFF00
```

## ☁️ Cloud Deployment

### AWS EC2

1. **Launch EC2 Instance**
   - Instance Type: t3.medium or larger
   - OS: Ubuntu 22.04 LTS
   - Storage: 20GB+
   - Security Group: Open ports 8000, 8501

2. **Install Docker**
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo usermod -aG docker $USER
   ```

3. **Deploy Application**
   ```bash
   git clone <repository-url>
   cd htw-emerging-photo
   docker-compose up -d
   ```

4. **Configure Firewall**
   ```bash
   sudo ufw allow 8000
   sudo ufw allow 8501
   sudo ufw enable
   ```

### Google Cloud Platform (GCP)

1. **Create Compute Engine Instance**
   - Machine Type: e2-medium or larger
   - OS: Ubuntu 22.04 LTS
   - Disk: 20GB+
   - Firewall: Allow HTTP/HTTPS

2. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Deploy Application**
   ```bash
   git clone <repository-url>
   cd htw-emerging-photo
   docker-compose up -d
   ```

### Azure VM

1. **Create Virtual Machine**
   - Size: Standard_B2s or larger
   - OS: Ubuntu 22.04 LTS
   - Disk: 30GB+
   - NSG: Allow ports 8000, 8501

2. **Install Docker**
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo systemctl enable docker
   ```

3. **Deploy Application**
   ```bash
   git clone <repository-url>
   cd htw-emerging-photo
   docker-compose up -d
   ```

## 🔒 Production Considerations

### Security

1. **Use HTTPS**
   - Set up reverse proxy (Nginx/Traefik)
   - Obtain SSL certificate (Let's Encrypt)
   - Redirect HTTP to HTTPS

2. **Environment Variables**
   - Never commit `.env` to version control
   - Use secrets management (AWS Secrets Manager, etc.)
   - Rotate credentials regularly

3. **Network Security**
   - Use firewall rules
   - Implement rate limiting
   - Set up VPC/private networks
   - Use API keys for authentication

4. **CORS Configuration**
   - Restrict allowed origins in production
   - Update `src/api/app.py`:
     ```python
     allow_origins=["https://yourdomain.com"]
     ```

### Performance

1. **Resource Allocation**
   - Backend: 2GB+ RAM, 2+ CPU cores
   - Frontend: 1GB+ RAM, 1+ CPU cores
   - Storage: 20GB+ for models and logs

2. **Optimization**
   - Use GPU for faster inference (optional)
   - Enable caching for model weights
   - Implement request queuing for high load
   - Use CDN for static assets

3. **Monitoring**
   - Set up health checks
   - Monitor CPU/RAM usage
   - Track API response times
   - Log errors and warnings

### Backup & Recovery

1. **Data Backup**
   - Model weights: Backup `data/models/`
   - Configuration: Backup `.env` and `docker-compose.yml`
   - Logs: Backup `logs/` directory

2. **Disaster Recovery**
   - Document deployment steps
   - Automate deployment with scripts
   - Test recovery procedures
   - Maintain multiple backups

## 🔧 Troubleshooting

### Container Issues

```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart

# Rebuild containers
docker-compose up --build --force-recreate
```

### Port Conflicts

```bash
# Check port usage
sudo lsof -i :8000
sudo lsof -i :8501

# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "8502:8501"  # Frontend
```

### Memory Issues

```bash
# Increase Docker memory limit
# Docker Desktop: Settings > Resources > Memory

# For Linux, edit /etc/docker/daemon.json
{
  "default-runtime": "runc",
  "default-ulimits": {
    "memlock": {
      "Hard": -1,
      "Name": "memlock",
      "Soft": -1
    }
  }
}
```

### Model Download Issues

```bash
# Manually download models
docker-compose exec backend python -c "
from src.detection import FaceDetector, PlateDetector
FaceDetector()
PlateDetector()
"
```

## 📊 Health Monitoring

### Health Check Endpoints

```bash
# Backend health
curl http://localhost:8000/health

# API info
curl http://localhost:8000/api/v1/info
```

### Monitoring Setup

1. **Prometheus + Grafana** (Advanced)
   - Add metrics endpoint
   - Configure Prometheus scraping
   - Create Grafana dashboards

2. **Simple Monitoring Script**
   ```bash
   #!/bin/bash
   while true; do
     curl -f http://localhost:8000/health || echo "Backend down!"
     sleep 60
   done
   ```

## 🚀 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker images
        run: |
          docker-compose build
          docker-compose push
      
      - name: Deploy to server
        run: |
          ssh user@server 'cd /app && docker-compose pull && docker-compose up -d'
```

## 📝 Deployment Checklist

- [ ] Docker and Docker Compose installed
- [ ] Repository cloned
- [ ] `.env` file configured
- [ ] Ports 8000 and 8501 available
- [ ] Sufficient disk space (20GB+)
- [ ] Sufficient RAM (4GB+)
- [ ] Firewall rules configured
- [ ] SSL certificate obtained (production)
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Health checks passing
- [ ] Documentation reviewed

## 🆘 Support

For deployment issues:
1. Check logs: `docker-compose logs`
2. Review troubleshooting section above
3. Consult main documentation in `docs/`
4. Contact development team

---

**Last Updated**: November 1, 2025  
**Version**: 1.0.0

