# Resume AI Analyzer - Deployment Guide

## 🚀 Deployment Options

### 1. Docker Deployment (Recommended)

#### Prerequisites
- Docker and Docker Compose installed
- At least 2GB RAM available
- Port 80 and 443 available

#### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd Resume-AI-main/App

# Build and run with Docker Compose
docker-compose up -d

# Access the application
http://localhost
```

#### Docker Commands
```bash
# Build the image
docker build -t resume-ai .

# Run the container
docker run -p 8501:8501 resume-ai

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### 2. Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Deployment Steps
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open the application
heroku open
```

#### Required Files for Heroku
- `Procfile` (included)
- `requirements-deploy.txt` (included)
- `runtime.txt` (create if needed)

### 3. PythonAnywhere Deployment

#### Prerequisites
- PythonAnywhere account
- Web application plan

#### Deployment Steps
1. Upload files to PythonAnywhere
2. Create virtual environment
3. Install dependencies
4. Configure web app
5. Set up WSGI configuration

### 4. AWS EC2 Deployment

#### Prerequisites
- AWS account
- EC2 instance (t2.micro or larger)

#### Deployment Steps
```bash
# Connect to EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Clone repository
git clone <repository-url>
cd Resume-AI-main/App

# Run with Docker
docker-compose up -d
```

### 5. Local Development Server

#### Quick Start
```bash
# Install dependencies
pip install -r requirements-deploy.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the application
streamlit run App_fixed.py
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# Server Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true

# Database (optional)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=cv
```

### SSL/HTTPS Setup

#### Using Nginx
1. Obtain SSL certificate
2. Update `nginx.conf` with SSL paths
3. Uncomment HTTPS section
4. Restart services

#### Using Let's Encrypt
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com
```

## 📊 Monitoring and Maintenance

### Health Checks
The application includes health checks at:
- `http://localhost:8501/_stcore/health`

### Log Management
```bash
# View application logs
docker-compose logs -f resume-ai

# View Nginx logs
docker-compose logs -f nginx
```

### Backup Strategy
- Regular database backups (if using MySQL)
- Backup uploaded resumes directory
- Version control for code changes

## 🔒 Security Considerations

### Production Security
1. Change default passwords
2. Use HTTPS in production
3. Implement rate limiting
4. Regular security updates
5. Monitor access logs

### File Upload Security
- File type validation
- Size limits
- Virus scanning
- Secure storage

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
sudo lsof -i :8501

# Kill process
sudo kill -9 <PID>
```

#### Memory Issues
- Increase container memory limits
- Optimize PDF processing
- Implement file cleanup

#### NLTK Data Missing
```bash
# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

#### spaCy Model Missing
```bash
# Download spaCy model
python -m spacy download en_core_web_sm
```

## 📈 Performance Optimization

### Database Optimization
- Use connection pooling
- Implement caching
- Regular maintenance

### Application Optimization
- Enable caching
- Optimize file uploads
- Use CDN for static assets

### Scaling Options
- Horizontal scaling with multiple containers
- Load balancing with Nginx
- Database replication

## 🔄 Updates and Maintenance

### Application Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Dependency Updates
```bash
# Update requirements
pip-review --local --interactive

# Rebuild container
docker-compose build --no-cache
```

## 📞 Support

For deployment issues:
1. Check logs for error messages
2. Verify all prerequisites are met
3. Ensure proper configuration
4. Test with minimal setup first

## 🎯 Quick Deployment Checklist

- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Ports available
- [ ] SSL configured (production)
- [ ] Health checks working
- [ ] Logs monitored
- [ ] Backup strategy in place
- [ ] Security measures implemented
