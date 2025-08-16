from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
    """Movie data model with all fields from CSV."""
    id: int
    title: str
    year: int
    genre: str
    director: str
    actors: str
    plot: str
    poster_url: str

class MovieResponse(BaseModel):
    """Response model for movie endpoints."""
    id: int
    title: str
    year: int
    genre: List[str]
    director: str
    actors: List[str]
    plot: str
    poster_url: str

class PaginatedMoviesResponse(BaseModel):
    """Response model for paginated movie lists."""
    movies: List[MovieResponse]
    page: int
    per_page: int
    total_movies: int
    total_pages: int

class SearchResponse(BaseModel):
    """Response model for search results."""
    movies: List[MovieResponse]
    query: dict
    total_results: int

class ApiKeyResponse(BaseModel):
    """Response model for API key information."""
    id: int
    owner_name: str
    key: str
    plan: str
    usage_count: int
    monthly_limit: int
    is_active: str
    created_at: str

class UsageStatsResponse(BaseModel):
    """Response model for usage statistics."""
    api_key: str
    owner_name: str
    plan: str
    usage_count: int
    monthly_limit: int
    usage_percentage: float
    endpoint_breakdown: dict
    period_days: int

class AdminStatsResponse(BaseModel):
    """Response model for admin statistics."""
    total_api_keys: int
    active_api_keys: int
    suspended_api_keys: int
    total_movies: int
    total_requests_today: int
    top_endpoints: dict

class CreateApiKeyRequest(BaseModel):
    """Request model for creating API key."""
    owner_name: str
    plan: Optional[str] = "free"
    monthly_limit: Optional[int] = 1000

class ResetUsageRequest(BaseModel):
    """Request model for resetting usage."""
    api_key: str
