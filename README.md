# Saleano - Product Search API

A FastAPI-based product search platform with AI-powered similarity search using vector embeddings.

## Features

- **Product Management**: Create and retrieve products with detailed information
- **AI-Powered Search**: Semantic similarity search using Google Gemini embeddings and PostgreSQL vector search
- **Modular Architecture**: Clean separation of models, routes, schemas, and utilities
- **Web Interface**: Basic HTML templates for homepage and about page
- **Database Integration**: PostgreSQL with SQLModel and pgvector for vector operations

## Tech Stack

- **Backend**: FastAPI, Python
- **Database**: PostgreSQL with pgvector extension
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **AI**: Google Gemini for embeddings
- **Templates**: Jinja2
- **Environment**: python-dotenv

## Prerequisites

- Python 3.8+
- PostgreSQL with pgvector extension
- Google Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd saleano
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   # or
   source env/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
   - Install PostgreSQL
   - Enable pgvector extension:
     ```sql
     CREATE EXTENSION vector;
     ```

## Configuration

1. Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```

2. Update the database URL in `src/db.py` if needed.

## Database Setup

Run the application once to create tables automatically, or manually:

```bash
python -c "from src.db import engine; from sqlmodel import SQLModel; SQLModel.metadata.create_all(engine)"
```

## Running the Application

Start the development server:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

- API Documentation: `http://127.0.0.1:8000/docs`
- Web Interface: `http://127.0.0.1:8000`

## API Endpoints

### Products

- `GET /products/` - Get all products
- `POST /products/` - Create a new product
- `GET /products/search?q=<query>&limit=<number>` - Search products by similarity

### Web Pages

- `GET /` - Homepage
- `GET /about` - About page


## Project Structure

```
src/
├── main.py              # Application entry point
├── db.py                # Database connection and session
├── lib/
│   └── gemini.py        # Gemini AI utilities
├── models/
│   ├── __init__.py
│   ├── product.py       # Product database model
│   └── user.py          # User database model
├── routes/
│   ├── __init__.py
│   ├── product.py       # Product API routes
│   └── user.py          # User API routes
├── schemas/
│   ├── __init__.py
│   └── product.py       # Pydantic schemas
├── static/              # Static files (CSS, JS, images)
└── templates/           # Jinja2 HTML templates
```

## Acknowledgments

- FastAPI for the web framework
- SQLModel for the ORM
- Google Gemini for AI embeddings
- pgvector for vector search in PostgreSQL
