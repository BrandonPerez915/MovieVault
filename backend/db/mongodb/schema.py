"""
Schema and index initialization module for MongoDB in MovieVault.
Defines JSON Schema validators for dedicated collections ('movies', 'reviews',
'users', 'actors', and 'directors') with foreign key references (ObjectId),
ensuring relational integrity in a document-based architecture.
"""

from typing import Dict, Any
from pymongo.database import Database
from pymongo import ASCENDING, DESCENDING, TEXT

from connection import MongoDBConnection

# JSON SCHEMA VALIDATORS
ACTORS_VALIDATOR: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "nationality", "is_active"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Full name of the actor/actress (required).",
            },
            "birth_year": {
                "bsonType": ["int", "null"],
                "description": "Year of birth.",
            },
            "nationality": {
                "bsonType": "string",
                "description": "Country of origin/nationality.",
            },
            "bio": {
                "bsonType": "string",
                "description": "Biographical summary.",
            },
            "is_active": {
                "bsonType": "bool",
                "description": "Whether the actor/actress is currently active in the industry.",
            },
        },
    }
}

DIRECTORS_VALIDATOR: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "nationality", "is_active"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Full name of the film director (required).",
            },
            "birth_year": {
                "bsonType": ["int", "null"],
                "description": "Year of birth.",
            },
            "nationality": {
                "bsonType": "string",
                "description": "Country of origin/nationality.",
            },
            "bio": {
                "bsonType": "string",
                "description": "Biographical summary.",
            },
            "is_active": {
                "bsonType": "bool",
                "description": "Whether the director is currently active in film production.",
            },
        },
    }
}

MOVIES_VALIDATOR: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "title",
            "release_year",
            "decade",
            "language",
            "genres",
            "countries",
            "directors",
            "cast",
            "synopsis",
            "rating",
            "ratings_count",
            "impact_score",
        ],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "Official title of the movie (required).",
            },
            "release_year": {
                "bsonType": "int",
                "minimum": 1888,
                "maximum": 2100,
                "description": "Release year (4-digit integer).",
            },
            "decade": {
                "bsonType": "int",
                "description": "Release decade (e.g. 1990 for 1994, 2000 for 2008).",
            },
            "language": {
                "bsonType": "object",
                "required": ["original", "availables"],
                "properties": {
                    "original": {"bsonType": "string"},
                    "availables": {"bsonType": "array", "items": {"bsonType": "string"}},
                },
                "description": "Language information with original and subtitle languages.",
            },
            "genres": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "List of movie genres.",
            },
            "countries": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "Country or countries of production.",
            },
            "directors": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["director_id", "name"],
                    "properties": {
                        "name": {"bsonType": "string"},
                        "id": {"bsonType": "objectId"},
                    },
                },
                "description": "Extended reference with director ObjectId and name.",
            },
            "cast": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["actor_id", "name"],
                    "properties": {
                        "name": {"bsonType": "string"},
                        "character": {"bsonType": "string"},
                        "id": {"bsonType": "objectId"},
                    },
                },
                "description": "Extended reference with actor ObjectId, name, and role.",
            },
            "synopsis": {
                "bsonType": "string",
                "description": "Plot summary or overview of the movie.",
            },
            "rating": {
                "bsonType": ["double", "int"],
                "minimum": 0.0,
                "maximum": 5.0,
                "description": "Average rating score (0.0 to 5.0).",
            },
            "ratings_count": {
                "bsonType": "int",
                "minimum": 0,
                "description": "Total count of rating submissions received.",
            },
            "impact_score": {
                "bsonType": ["double", "int"],
                "description": "Calculated impact metric: avg_rating * log10(1 + total_ratings).",
            },
        },
    }
}

REVIEWS_VALIDATOR: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "movie",
            "owner",
            "rating",
            "content",
            "likes",
            "comments_count",
            "created_at",
        ],
        "properties": {
            "movie": {
                "bsonType": "object",
                "required": ["id", "title"],
                "properties": {
                    "title": {"bsonType": "string"},
                    "id": {"bsonType": "objectId"},
                },
                "description": "Embedded movie information for quick access.",
            },
            "owner": {
                "bsonType": "object",
                "required": ["id", "username"],
                "properties": {
                    "id": {"bsonType": "objectId"},
                    "username": {"bsonType": "string"},
                },
                "description": "Embedded owner information for quick access.",
            },
            "rating": {
                "bsonType": ["double", "int"],
                "minimum": 0.5,
                "maximum": 5.0,
                "description": "Optional numeric rating awarded (0.5 to 5.0).",
            },
            "content": {
                "bsonType": "string",
                "description": "Text content of the review.",
            },
            "likes": {
                "bsonType": "int",
                "minimum": 0,
                "description": "Total number of likes received.",
            },
            "comments_count": {
                "bsonType": "int",
                "minimum": 0,
                "description": "Number of comments attached to the review.",
            },
            "created_at": {
                "bsonType": "date",
                "description": "Timestamp when the review was created.",
            },
        },
    }
}

USERS_VALIDATOR: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "email", "created_at", "lists"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "Unique username handle.",
            },
            "email": {
                "bsonType": "string",
                "description": "Unique email address.",
            },
            "created_at": {
                "bsonType": "date",
                "description": "Account registration timestamp.",
            },
            "lists": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["name", "movies"],
                    "properties": {
                        "name": {"bsonType": "string"},
                        "movies": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "object",
                                "required": ["id", "title"],
                                "properties": {
                                    "id": {"bsonType": "objectId"},
                                    "title": {"bsonType": "string"},
                                    "poster_url": {"bsonType": "string"},  
                                }
                            },
                        },
                    },
                },
                "description": "User-defined lists of favorite or watchlisted movies.",
            }
        },
    }
}

LISTS_VALIDATOR: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["owner", "name", "movies"],
        "properties": {
            "owner": {
                "bsonType": "object",
                "required": ["id", "username"],
                "properties": {
                    "username": {"bsonType": "string"},
                    "id": {"bsonType": "objectId"},
                },
                "description": "Embedded owner information for quick access.",
            },
            "name": {
                "bsonType": "string",
                "description": "Name of the user-defined list.",
            },
            "movies": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["title", "id"],
                    "properties": {
                        "id": {"bsonType": "objectId"},
                        "title": {"bsonType": "string"},
                        "poster_url": {"bsonType": "string"},
                    },
                },
                "description": "Array of movie references with embedded details for quick access.",
            },
        },
    }
}


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


def setup_schema(database: Database = None) -> Database:
    """Entry point to initialize all collections and indexes in MongoDB."""
    if database is None:
        database = MongoDBConnection().database

    print(f"Initializing schema on database: '{database.name}'...")
    create_collection(database, "actors", ACTORS_VALIDATOR)
    create_collection(database, "directors", DIRECTORS_VALIDATOR)
    create_collection(database, "movies", MOVIES_VALIDATOR)
    create_collection(database, "reviews", REVIEWS_VALIDATOR)
    create_collection(database, "users", USERS_VALIDATOR)
    create_collection(database, "lists", LISTS_VALIDATOR)
    create_indexes(database)
    print("Schema initialization completed successfully.")
    return database


if __name__ == "__main__":
    setup_schema()
