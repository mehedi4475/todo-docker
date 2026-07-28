# Todo API — Dockerized with Full CI/CD and HTTPS

A simple to-do list REST API built with Flask and PostgreSQL, fully containerized with Docker and deployed to a remote VPS through a complete CI/CD pipeline. It runs behind an Nginx reverse proxy with a free Let's Encrypt SSL certificate, served over HTTPS on a custom subdomain. Every push to `main` automatically builds a new image, publishes it to Docker Hub, and deploys it to the live server — no manual steps.

**Live:** https://todo.yourdomain.com

## Tech Stack

- **Python (Flask)** — REST API
- **PostgreSQL** — database
- **Docker & Docker Compose** — containerization
- **GitHub Actions** — CI/CD pipeline
- **Ubuntu VPS** — deployment target
- **Nginx** — reverse proxy
- **Let's Encrypt / Certbot** — free SSL/HTTPS

## What This Project Demonstrates

- Writing a Dockerfile with layer caching best practices
- Running an app and a database as connected containers
- Passing configuration via environment variables (no hardcoded secrets)
- Persisting database data using Docker volumes
- Automating image builds and pushes with CI/CD
- Storing credentials securely with GitHub Actions secrets
- Deploying to a remote server over SSH from within the pipeline
- Following the principle of least privilege — deploying via a dedicated non-root user
- Setting up an Nginx reverse proxy and securing a subdomain with a free Let's Encrypt SSL certificate, with automatic renewal

## Architecture / Flow
'''
Developer push to main
│
▼
GitHub Actions
├── Build Docker image
├── Push image to Docker Hub
└── SSH into VPS → pull new image → restart containers
│
▼
User → https://todo.yourdomain.com (443, SSL)
│
▼
Nginx (reverse proxy)
│
▼
App container (localhost:5000)
'''

## Prerequisites

- Docker
- Docker Compose

## How to Run Locally

```bash
git clone https://github.com/mehedi4475/todo-docker.git
cd todo-docker
docker compose up --build
```

The API will be available at `http://localhost:5000`.

## Run from Docker Hub

```bash
docker pull mehedi4475/todo-docker:latest
```

## API Endpoints

| Method | Endpoint | Description    |
|--------|----------|----------------|
| GET    | /todos   | List all todos |
| POST   | /todos   | Add a new todo |

## Usage Examples

```bash
# Add a todo
curl -X POST https://todo.yourdomain.com/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "Learn Docker"}'

# List all todos
curl https://todo.yourdomain.com/todos
```

## CI/CD Pipeline

Defined in `.github/workflows/ci.yml`. On every push to `main`, the pipeline automatically:

1. Checks out the code
2. Logs in to Docker Hub using stored secrets
3. Builds the Docker image
4. Pushes the image to Docker Hub (`latest` tag)
5. Connects to the VPS over SSH and redeploys:
   - Pulls the new image
   - Restarts the containers
   - Cleans up old unused images

Deployment uses a dedicated non-root user (`deployer`) and a separate SSH key created specifically for the pipeline, following the principle of least privilege.

## Infrastructure & Hosting

- Hosted on an **Ubuntu VPS**
- **Nginx** acts as a reverse proxy, forwarding HTTPS traffic to the app container on port 5000
- **Let's Encrypt** provides a free SSL certificate (via Certbot), with automatic renewal enabled
- Only ports 80/443 (web) and 22 (SSH) are exposed; the app port is not directly reachable from outside

## Project Structure
'''
todo-docker/
├── .github/
│ └── workflows/
│ └── ci.yml # CI/CD pipeline
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── Dockerfile # Container image definition
├── docker-compose.yml # Multi-container setup
└── README.md
'''

## What I Learned

- How Docker builds images in layers, and why dependency files are copied before code.
- How containers talk to each other over a shared network using service names.
- Why volumes are needed to keep database data across restarts.
- How a CI/CD pipeline removes manual work end to end — from code to a running server.
- How to keep credentials safe using secrets instead of hardcoding them.
- How one machine can securely run commands on another over SSH, and why a dedicated non-root user with its own key is safer than using root.
- How to recover a broken package system on Ubuntu (`dpkg --configure -a`).
- How to put an app behind an Nginx reverse proxy and secure it with a free, auto-renewing SSL certificate.

## Possible Next Steps

- Add automated tests as a pipeline gate before deploy
- Provision the VPS/infrastructure with Terraform
- Add health checks and monitoring (Prometheus + Grafana)
- Move configuration to a `.env` file or secrets manager
- Add Kubernetes manifests for orchestration