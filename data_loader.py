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
import csv
import os
from sqlalchemy.orm import Session
from db.database import SessionLocal, create_tables
from db.models_v3 import Movie

def load_movies_from_csv():
    """Load movies from CSV file into database."""
    db = SessionLocal()
    try:
        # Check if movies already exist
        existing_count = db.query(Movie).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} movies. Skipping CSV import.")
            return

        csv_file = "data/movies.csv"
        if not os.path.exists(csv_file):
            print(f"CSV file {csv_file} not found. Creating sample movies...")
            create_sample_movies(db)
            return

        print("Loading movies from CSV...")
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            movies_added = 0

            for row in csv_reader:
                # Create movie object
                movie = Movie(
                    title=row.get('title', '').strip(),
                    year=int(row.get('year', 0)) if row.get('year', '').strip().isdigit() else None,
                    genre=row.get('genre', '').strip(),
                    director=row.get('director', '').strip(),
                    actors=row.get('actors', '').strip(),
                    plot=row.get('plot', '').strip(),
                    poster_url=row.get('poster_url', '').strip()
                )

                db.add(movie)
                movies_added += 1

                if movies_added % 100 == 0:
                    db.commit()
                    print(f"Loaded {movies_added} movies...")

            db.commit()
            print(f"Successfully loaded {movies_added} movies from CSV!")

    except Exception as e:
        print(f"Error loading movies: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_movies(db: Session):
    """Create sample movies for testing."""
    sample_movies = [
        {
            "title": "The Shawshank Redemption",
            "year": 1994,
            "genre": "Drama",
            "director": "Frank Darabont",
            "actors": "Tim Robbins|Morgan Freeman|Bob Gunton",
            "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg"
        },
        {
            "title": "The Godfather",
            "year": 1972,
            "genre": "Crime|Drama",
            "director": "Francis Ford Coppola",
            "actors": "Marlon Brando|Al Pacino|James Caan",
            "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg"
        },
        {
            "title": "Pulp Fiction",
            "year": 1994,
            "genre": "Crime|Drama",
            "director": "Quentin Tarantino",
            "actors": "John Travolta|Uma Thurman|Samuel L. Jackson",
            "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg"
        },
        {
            "title": "The Dark Knight",
            "year": 2008,
            "genre": "Action|Crime|Drama",
            "director": "Christopher Nolan",
            "actors": "Christian Bale|Heath Ledger|Aaron Eckhart",
            "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg"
        },
        {
            "title": "Forrest Gump",
            "year": 1994,
            "genre": "Drama|Romance",
            "director": "Robert Zemeckis",
            "actors": "Tom Hanks|Robin Wright|Gary Sinise",
            "plot": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg"
        }
    ]

    for movie_data in sample_movies:
        movie = Movie(**movie_data)
        db.add(movie)

    db.commit()
    print(f"Created {len(sample_movies)} sample movies!")

if __name__ == "__main__":
    create_tables()
    load_movies_from_csv()