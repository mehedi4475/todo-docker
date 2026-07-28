# Todo API — Dockerized with CI/CD

A simple to-do list REST API built with Flask and PostgreSQL, fully containerized with Docker and automatically built and published to Docker Hub through a GitHub Actions CI/CD pipeline. This is a DevOps portfolio project focused on containerization and automation fundamentals.

## Tech Stack

- **Python (Flask)** — REST API
- **PostgreSQL** — database
- **Docker** — containerization
- **Docker Compose** — multi-container orchestration
- **GitHub Actions** — CI/CD pipeline

## What This Project Demonstrates

- Writing a Dockerfile with layer caching best practices
- Running an app and a database as separate, connected containers
- Passing configuration via environment variables (no hardcoded secrets)
- Persisting database data using Docker volumes
- Automating image builds and pushes with a CI/CD pipeline
- Storing credentials securely using GitHub Actions secrets

## Prerequisites

- Docker
- Docker Compose

## How to Run Locally

Clone the repository and start the containers:

```bash
git clone https://github.com/mehedi4475/todo-docker.git
cd todo-docker
docker compose up --build
```

The API will be available at `http://localhost:5000`.

## Run from Docker Hub

The image is automatically published to Docker Hub on every push to `main`:

```bash
docker pull mehedi4475/todo-docker:latest
```

## API Endpoints

| Method | Endpoint | Description    |
|--------|----------|----------------|
| GET    | /todos   | List all todos |
| POST   | /todos   | Add a new todo |

## Usage Examples

Add a new todo:

```bash
curl -X POST http://localhost:5000/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "Learn Docker"}'
```

List all todos:

```bash
curl http://localhost:5000/todos
```

## CI/CD Pipeline

This project uses GitHub Actions. On every push to the `main` branch, the pipeline automatically:

1. Checks out the code
2. Logs in to Docker Hub using securely stored secrets
3. Builds the Docker image
4. Pushes the image to Docker Hub with the `latest` tag

The workflow is defined in `.github/workflows/ci.yml`.

## Project Structure
```

todo-docker/
├── .github/
│ └── workflows/
│ └── ci.yml # CI/CD pipeline
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── Dockerfile # Container image definition
├── docker-compose.yml # Multi-container setup
└── README.md
## What I Learned

- How Docker builds images layer by layer, and why copying `requirements.txt` before the rest of the code speeds up rebuilds.
- How containers communicate over a shared network (the app reaches the database using the service name `db`).
- Why volumes matter — without them, database data is lost on every restart.
- How a CI/CD pipeline removes manual work by building and publishing the image automatically on every push.
- How to keep credentials out of code by using GitHub Actions secrets.

## Next Steps

- Deploy the container to a cloud provider (AWS EC2)
- Provision the infrastructure using Terraform
- Add Kubernetes manifests for orchestration
- Add automated tests to the pipeline