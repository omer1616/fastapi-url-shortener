# URL Shortener

URL Shortener is a web application that allows users to shorten long URLs and redirect to the original URLs using shortened versions. This application is built with FastAPI and includes caching and database integration for optimal performance.

## Features

- Shorten long URLs to short, easy-to-share versions.
- Redirect users from shortened URLs to the original URLs.
- Store and retrieve URL data using an SQLite/PostgreSQL database.
- Cache URLs in Redis for improved performance.
- Basic error handling for invalid or non-existent URLs.
- Unit tests to verify the functionality of the application.

## Requirements

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Redis
- Pydantic



## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/omer1616/fastapi-url-shortener.git
```
### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
### 3.  Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables

```bash
DATABASE_URL=sqlite:///./test.db  # Or use PostgreSQL: postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
BASE_URL=http://localhost:8000
```
### 5. Start the Redis Server

```bash
redis-server
```
### Running the Application

## 1. Start the FastAPI Server
```bash
python run.py
```

## 1. Start the FastAPI Server
```bash
python run.py
```

## 2. Shorten a URL
- You can shorten a URL using a POST request:
```bash
curl -X POST "http://localhost:8000/shorten" -H "Content-Type: application/json" -d '{"original_url": "http://example.com"}'
```
## 3. Access the Shortened URL
- Visit the shortened URL to be redirected to the original URL::
```bash
http://localhost:8000/{short_url}

```
## Testing
- Run the unit tests with:
```bash
pytest
```
## Documentation
FastAPI automatically generates interactive API documentation. After starting the server, you can access it at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

