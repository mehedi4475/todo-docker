# Todo API — Dockerized with PostgreSQL

A simple to-do list REST API built with Flask and PostgreSQL, fully containerized using Docker and Docker Compose. This is my first DevOps portfolio project, focused on learning containerization fundamentals.

## Tech Stack

- **Python (Flask)** — REST API
- **PostgreSQL** — database
- **Docker** — containerization
- **Docker Compose** — multi-container orchestration

## What This Project Demonstrates

- Writing a Dockerfile with layer caching best practices
- Running an app and a database as separate, connected containers
- Passing configuration via environment variables (no hardcoded secrets)
- Persisting database data using Docker volumes

## Prerequisites

- Docker
- Docker Compose

## How to Run

Clone the repository and start the containers:

```bash
git clone https://github.com/mehedi4475/todo-docker.git
cd todo-docker
docker compose up --build
```

The API will be available at `http://localhost:5000`.

## API Endpoints

| Method | Endpoint | Description        |
|--------|----------|--------------------|
| GET    | /todos   | List all todos     |
| POST   | /todos   | Add a new todo     |

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

## Project Structure
todo-docker/
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── Dockerfile # Container image definition
├── docker-compose.yml # Multi-container setup
└── README.md


## What I Learned

- How Docker images are built layer by layer, and why copying `requirements.txt` before the rest of the code speeds up rebuilds.
- How containers communicate over a shared network (the app reaches the database using the service name `db`).
- Why volumes matter — without them, database data is lost every time the container restarts.

## Next Steps

- Add a CI/CD pipeline with GitHub Actions to auto-test and build the image
- Deploy to a cloud provider (AWS)
- Add Kubernetes manifests