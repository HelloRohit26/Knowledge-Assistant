# Enterprise Knowledge Intelligence Platform — Production Deployment Guide

Complete step-by-step guide for deploying the platform using Docker, Docker Compose, Nginx, HTTPS, and Cloud Providers.

---

## 1. Prerequisites

- **Docker Engine** (v24.0+) & **Docker Compose** (v2.20+)
- **Domain Name** (for HTTPS setup)
- **Gemini API Key** from Google AI Studio

---

## 2. Quick Local / Server Deployment (Docker Compose)

### Step 1: Clone & Configure Environment
```bash
git clone <repository_url>
cd Knowledge_Assistant

# Copy environment template
cp .env.production.example .env
```

Edit `.env` and insert your production keys:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
SECRET_KEY=generate_random_64_character_secret_string
```

### Step 2: Build & Start Services
```bash
docker-compose up -d --build
```

### Step 3: Verify Health
```bash
# Check running containers
docker-compose ps

# View backend health
curl http://localhost:8000/api/registry/health

# Access frontend dashboard
# Open http://localhost/ in your browser
```

---

## 3. Production Nginx & HTTPS Setup (Let's Encrypt / Certbot)

For internet-facing cloud servers (AWS EC2, DigitalOcean Droplet, GCP Compute):

### Nginx SSL Configuration (`/etc/nginx/conf.d/knowledge_assistant.conf`)

```nginx
server {
    listen 80;
    server_name knowledge.yourcompany.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name knowledge.yourcompany.com;

    ssl_certificate /etc/letsencrypt/live/knowledge.yourcompany.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/knowledge.yourcompany.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### Enable SSL with Certbot
```bash
sudo apt update && sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d knowledge.yourcompany.com
```

---

## 4. Cloud Deployment Options

### Option A: AWS EC2 / DigitalOcean (Recommended)
1. Provision Ubuntu 22.04 LTS instance (2 vCPU, 4GB RAM minimum).
2. Install Docker & Docker Compose.
3. Clone repo, setup `.env`, run `docker-compose up -d --build`.
4. Point DNS A-record to instance IP and configure Certbot HTTPS.

### Option B: Render / Railway (PaaS)
1. Deploy **Backend** service using `./backend/Dockerfile`. Set `GEMINI_API_KEY` and `CHROMA_DB_PATH=/tmp/chroma_db` in environment variables.
2. Deploy **Frontend** static service using `./frontend/Dockerfile`.

---

## 5. Maintenance & Logs

```bash
# View live backend logs
docker-compose logs -f backend

# View live frontend logs
docker-compose logs -f frontend

# Re-index data folder
curl -X POST http://localhost:8000/api/registry/reindex
```
