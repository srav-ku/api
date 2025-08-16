import pandas as pd
from typing import List, Dict, Any
from models import Movie, MovieResponse

class MovieDataLoader:
    """Handles loading and managing movie data from CSV file."""
    
    def __init__(self, csv_path: str = "data/movies.csv"):
        self.csv_path = csv_path
        self.movies: List[Movie] = []
        self.movies_dict: Dict[int, Movie] = {}
        
    def load_data(self) -> None:
        """Load movie data from CSV file into memory."""
        try:
            df = pd.read_csv(self.csv_path)
            
            for _, row in df.iterrows():
                movie = Movie(
                    id=int(row['id']),
                    title=str(row['title']),
                    year=int(row['year']),
                    genre=str(row['genre']),
                    director=str(row['director']),
                    actors=str(row['actors']),
                    plot=str(row['plot']),
                    poster_url=str(row['poster_url'])
                )
                self.movies.append(movie)
                self.movies_dict[movie.id] = movie
                
            print(f"Loaded {len(self.movies)} movies from {self.csv_path}")
            
        except FileNotFoundError:
            print(f"Error: CSV file not found at {self.csv_path}")
            raise
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            raise
    
    def get_all_movies(self) -> List[Movie]:
        """Get all movies."""
        return self.movies
    
    def get_movie_by_id(self, movie_id: int) -> Movie:
        """Get a specific movie by ID."""
        return self.movies_dict.get(movie_id)
    
    def search_movies(self, title: str = None, year: int = None, genre: str = None) -> List[Movie]:
        """Search movies by title, year, and/or genre."""
        results = self.movies.copy()
        
        if title:
            title_lower = title.lower()
            results = [movie for movie in results if title_lower in movie.title.lower()]
        
        if year:
            results = [movie for movie in results if movie.year == year]
        
        if genre:
            genre_lower = genre.lower()
            results = [movie for movie in results 
                      if any(genre_lower in g.lower() for g in movie.genre.split('|'))]
        
        return results
    
    @staticmethod
    def movie_to_response(movie: Movie) -> MovieResponse:
        """Convert Movie model to MovieResponse model."""
        return MovieResponse(
            id=movie.id,
            title=movie.title,
            year=movie.year,
            genre=movie.genre.split('|'),
            director=movie.director,
            actors=movie.actors.split('|'),
            plot=movie.plot,
            poster_url=movie.poster_url
        )
