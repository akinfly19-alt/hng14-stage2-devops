# HNG14 Stage 2 DevOps — Job Processing System

A containerised job processing system with a Node.js frontend, Python/FastAPI backend, and Python worker connected via Redis.

## Prerequisites

- Docker v24+
- Docker Compose v2.20+
- Git

## Quick Start

### 1. Clone the repository
### 2. Create your .env file
Open .env and set a strong Redis password.

### 3. Build and start all services
### 4. Verify everything is running
All four services should show status: healthy

### 5. Open the application
Navigate to http://localhost:3000

Click Submit New Job. The job will appear as queued then completed within seconds.

## Architecture

Browser -> Frontend (Node.js :3000) -> API (FastAPI :8000) -> Redis (internal)
                                                                      ^
                                                                      |
                                                             Worker (Python)

Redis is NOT exposed to the host. All services communicate on the internal Docker network.

## Running Tests
## Stopping the Stack
## CI/CD Pipeline

lint -> test -> build -> security -> integration -> deploy

A failure in any stage blocks all subsequent stages.
Deploy stage runs on main branch pushes only.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| REDIS_PASSWORD | Yes | Redis authentication password |
| APP_ENV | No | Application environment (default: production) |
| FRONTEND_PORT | No | Host port for frontend (default: 3000) |
