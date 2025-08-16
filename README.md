# Movie API Backend

A FastAPI backend providing movie search and listing endpoints with CSV data source and in-memory storage.

## Features

- **Movie Listing**: Get all movies with pagination (10 movies per page by default)
- **Movie Search**: Search movies by title, year, genre, or combinations
- **Movie Details**: Get detailed information about a specific movie by ID
- **CSV Data Source**: Loads movie data from CSV file into memory for fast access
- **Clean JSON Responses**: Consistent, well-structured API responses

## API Endpoints

### 1. GET /movies
List all movies with pagination support.

**Parameters:**
- `page` (optional): Page number (default: 1, minimum: 1)
- `per_page` (optional): Movies per page (default: 10, maximum: 50)

**Example:**
```bash
curl "http://localhost:8000/movies?page=1&per_page=10"
