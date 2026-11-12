"""
Schema and index initialization module for MongoDB in MovieVault.
Defines JSON Schema validators for dedicated collections ('movies', 'reviews',
'users', 'actors', and 'directors') with foreign key references (ObjectId),
ensuring relational integrity in a document-based architecture.
"""

from typing import Dict, Any
from pymongo.database import Database
from pymongo import ASCENDING, DESCENDING, TEXT

from databases.mongodb.connection import MongoConnection
from databases.mongodb.validators import (
    ACTORS_VALIDATOR,
    DIRECTORS_VALIDATOR,
    MOVIES_VALIDATOR,
    REVIEWS_VALIDATOR,
    USERS_VALIDATOR,
    LISTS_VALIDATOR,
)

class MongoSchema:
    """
    Provides methods to create collections with validation and to establish
    indexes that optimize query performance across the MovieVault application.
    """

    def __new__(cls):
        raise NotImplementedError("MongoSchema is a static utility class and cannot be instantiated.")

    def __init__(self):
        raise NotImplementedError("MongoSchema is a static utility class and cannot be instantiated.")


    @staticmethod
    def create_collection(
        database: Database,
        name: str,
        validator: Dict[str, Any]
    ) -> None:
        """Creates a collection with a JSON Schema validator or updates it if it already exists."""
        collections = database.list_collection_names()
        if name not in collections:
            database.create_collection(name, validator=validator)
            print(f"Collection '{name}' created with JSON Schema validator.")
        else:
            database.command(
                "collMod",
                name,
                validator=validator,
                validationLevel="moderate",
            )
            print(f"Validator for collection '{name}' updated successfully.")


    @staticmethod
    def create_indexes(database: Database) -> None:
        """
        Creates optimal indexes in MongoDB to satisfy the requirements across collections:
        - actors: index on name
        - directors: index on name
        - movies:
            compound indexes for decade/language.original/impact, genre/country/impact,rating/directors.name/decade/impact, movie.title/synopsis/impact, cast.name/impact, directors.name/impact, and single-field index on impact_score.
        - reviews: content/movie.title/likes/comments, owner.username/created_at
        - users: unique on username and email
        """
        # INDEXES FOR 'actors' COLLECTION
        actors = database["actors"]
        actors.create_index([("name", ASCENDING)], name="idx_actors_name")

        # INDEXES FOR 'directors' COLLECTION
        directors = database["directors"]
        directors.create_index([("name", ASCENDING)], name="idx_directors_name")

        # INDEXES FOR 'movies' COLLECTION
        movies = database["movies"]
        # Requirement 1: Search by title, decade range, and language, sorted by impact
        movies.create_index(
            [
                ("decade", ASCENDING),
                ("language.original", ASCENDING),
                ("impact_score", DESCENDING),
            ],
            name="idx_decade_lang_impact",
        )

        # Requirement 2: Filter by genre, country, sorted by impact
        movies.create_index(
            [("genres", ASCENDING),("impact_score", DESCENDING),],
            name="idx_genre_impact",
        )
        movies.create_index(
            [("countries", ASCENDING),("impact_score", DESCENDING),],
            name="idx_country_impact",
        )

        # Requirement 3: Filter by rating, director, decade, sorted by impact
        movies.create_index(
            [
                ("rating", ASCENDING),
                ("directors.name", ASCENDING),
                ("decade", ASCENDING),
                ("impact_score", DESCENDING),
            ],
            name="idx_rating_director_decade_impact",
        )

        # Requirement 4: Keyword search on movie title, synopsis, sorted by impact
        movies.create_index(
            [
                ("title", TEXT),
                ("synopsis", TEXT),
                ("impact_score", DESCENDING),
            ],
            default_language="spanish",
            name="idx_title_synopsis_impact",
        )

        # Requirement 6: Indexes for cast actor name and director name, sorted by impact score
        movies.create_index(
            [("cast.name", ASCENDING), ("impact_score", DESCENDING)],
            name="idx_cast_name_impact",
        )
        movies.create_index(
            [("directors.name", ASCENDING), ("impact_score", DESCENDING)],
            name="idx_directors_name_impact",
        )

        # Single-field index on impact score
        movies.create_index([("impact_score", DESCENDING)], name="idx_impact_score")

        # INDEXES FOR 'reviews' COLLECTION
        reviews = database["reviews"]
        # Requirement 5: Reviews for a movie, sorted by likes and comments count
        reviews.create_index(
            [
                ("movie.title", ASCENDING),
                ("likes", DESCENDING),
                ("comments_count", DESCENDING),
            ],
            name="idx_movie_likes_comments",
        )

        # Requirement 5: Keyword text search on review content
        reviews.create_index(
            [("content", TEXT)],
            default_language="spanish",
            name="idx_text_review_content",
        )

        # User historical reviews lookup
        reviews.create_index(
            [("owner.username", ASCENDING), ("created_at", ASCENDING)],
            name="idx_username_created_at",
        )

        # INDEXES FOR 'users' COLLECTION
        users = database["users"]
        users.create_index([("username", ASCENDING)], unique=True, name="idx_unique_username")
        users.create_index([("email", ASCENDING)], unique=True, name="idx_unique_email")

        print("All required indexes across all collections created successfully.")


    @staticmethod
    def setup(self, database: Database = None) -> Database:
        """Entry point to initialize all collections and indexes in MongoDB."""
        if database is None:
            database = MongoConnection().database

        print(f"Initializing schema on database: '{database.name}'...")
        self.create_collection(database, "actors", ACTORS_VALIDATOR)
        self.create_collection(database, "directors", DIRECTORS_VALIDATOR)
        self.create_collection(database, "movies", MOVIES_VALIDATOR)
        self.create_collection(database, "reviews", REVIEWS_VALIDATOR)
        self.create_collection(database, "users", USERS_VALIDATOR)
        self.create_collection(database, "lists", LISTS_VALIDATOR)
        self.create_indexes(database)
        print("Schema initialization completed successfully.")
        return database
