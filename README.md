AI Book Management System

An AI-powered, cloud-ready book management system built with FastAPI, async PostgreSQL, OpenRouter LLM (Llama-3), and DigitalOcean Spaces.
The system supports user registration, authentication, book uploads, reviews, AI-generated summaries, and recommendations, with full unit & integration testing and CI/CD.

 Features

 User registration & login (JWT authentication)

 CRUD operations for books

 Book file storage using DigitalOcean Spaces

 User reviews & ratings

 AI-generated:

Book summaries

Review summaries

Book recommendations

 Fully async (FastAPI + SQLAlchemy + asyncpg)

 Docker & cloud-ready

 Unit  tests

 CI/CD via GitHub Actions

 Auto-generated API docs (Swagger)

 Architecture Overview
Client (Swagger / REST)
        |
     FastAPI
        |
 PostgreSQL (metadata, users, reviews)
        |
 DigitalOcean Spaces (book files)
        |
 OpenRouter (Llama-3-8B)

 Tech Stack
Layer	Technology
Backend	FastAPI (Python 3.11)
Database	PostgreSQL (asyncpg)
ORM	SQLAlchemy (async)
Authentication	JWT (OAuth2 Password Flow)
Password Hashing	Argon2 (OWASP recommended)
AI / LLM	OpenRouter (Llama-3-8B)
Storage	DigitalOcean Spaces (S3 compatible)
Containerization	Docker & Docker Compose
Testing	Pytest, pytest-asyncio
CI/CD	GitHub Actions
 Project Structure
ai-book-management/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── security.py
│   │
│   ├── services/
│   │   ├── llm_client.py
│   │   ├── storage.py
│   │   └── text_extractor.py
│   │
│   └── routes/
│       ├── auth.py
│       ├── books.py
│       ├── recommendations.py
│       └── ai.py
│
├── tests/
│   ├── unit/
│   
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md

 Authentication Flow

Register

POST /auth/register


Login

POST /auth/login


Uses OAuth2 Password Flow (form-encoded)

Returns JWT access token

Authorize

Swagger UI → Click Authorize

Paste JWT token

Access Protected APIs

Authorization: Bearer <token>

 API Endpoints
Authentication

POST /auth/register

POST /auth/login

Books

POST /books (upload book file to Spaces)

GET /books

GET /books/{id}

PUT /books/{id}

DELETE /books/{id}

Reviews

POST /books/{id}/reviews

GET /books/{id}/reviews

AI

GET /books/{id}/summary

GET /recommendations?preferences=...

POST /generate-summary

DigitalOcean Spaces (File Storage)

Book files (PDF / TXT) are stored in DigitalOcean Spaces

Only the storage path is stored in PostgreSQL

Files are not stored locally

Text is extracted before sending to the AI model

Benefits:

Scalable

Cloud-native

S3 compatible

Easy migration to AWS S3

 AI Model

Provider: OpenRouter

Model: meta-llama/llama-3-8b-instruct

Integrated using LangChain

No local model download required

 Environment Variables

Create a .env file using the example below:

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/books
JWT_SECRET=supersecretkey

OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

DO_SPACES_KEY=your_spaces_key
DO_SPACES_SECRET=your_spaces_secret
DO_SPACES_BUCKET=books-storage
DO_SPACES_REGION=blr1
DO_SPACES_ENDPOINT=https://blr1.digitaloceanspaces.com

 Run with Docker
docker-compose up --build


API Docs:

http://localhost:8000/docs

Running Tests
pytest


Tests include:

Authentication

Book CRUD

Reviews

AI services (mocked)

Storage integration (mocked)