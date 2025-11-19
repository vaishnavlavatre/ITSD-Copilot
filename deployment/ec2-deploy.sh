#!/bin/bash

echo "🚀 Starting ITSD Copilot Deployment on EC2..."
echo "=============================================="

# Update system
echo "📦 Updating system packages..."
sudo yum update -y

# Install Docker
echo "🐳 Installing Docker..."
sudo yum install docker -y

# Start Docker service
echo "🔧 Starting Docker service..."
sudo service docker start
sudo systemctl enable docker

# Add ec2-user to docker group
echo "👤 Adding ec2-user to docker group..."
sudo usermod -a -G docker ec2-user

# Install Docker Compose
echo "📋 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create app directory
echo "📁 Creating application directory..."
mkdir -p /home/ec2-user/itsd-copilot
cd /home/ec2-user/itsd-copilot

# Copy application files (this assumes you'll upload files separately)
echo "📄 Setting up application structure..."
mkdir -p backend frontend knowledge_base

# Create Dockerfiles
echo "🐳 Creating Dockerfiles..."

# Backend Dockerfile
cat > backend/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p knowledge_base
EXPOSE 5000
CMD ["python", "run.py"]
EOF

# Frontend Dockerfile
cat > frontend/Dockerfile << 'EOF'
FROM nginx:alpine
COPY . /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# Frontend nginx config
cat > frontend/nginx.conf << 'EOF'
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /api/ {
        proxy_pass http://backend:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./knowledge_base:/app/knowledge_base
    environment:
      - FLASK_ENV=production
      - JWT_SECRET_KEY=itsd-copilot-production-secret-2024
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
EOF

echo "✅ Basic setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Upload your application files to /home/ec2-user/itsd-copilot/"
echo "2. Run: cd /home/ec2-user/itsd-copilot && docker-compose up --build -d"
echo "3. Your app will be available at: http://YOUR_EC2_IP"