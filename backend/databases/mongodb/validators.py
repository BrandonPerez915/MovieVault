from typing import Dict, Any

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
            "poster_url",
            "decade",
            "language",
            "genres",
            "countries",
            "directors",
            "cast",
            "synopsis",
            "rating",
            "ratings_count",
            "likes",
            "awards",
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
            "poster_url": {
                "bsonType": "string",
                "description": "URL to the movie's poster image.",
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
            "likes": {
                "bsonType": "int",
                "minimum": 0,
                "description": "Total number of likes received.",
            },
            "awards": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "List of awards won or nominated for.",
            },
            "impact_score": {
                "bsonType": ["double", "int"],
                "description": "Calculated impact metric: avg_rating * log10(1 + total_ratings).",
            },
            "available_streaming": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "List of streaming platforms where the movie is available.",
            }
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
        "required": ["username", "email", "password_hash", "created_at", "lists"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "Unique username handle.",
            },
            "email": {
                "bsonType": "string",
                "description": "Unique email address.",
            },
            "password_hash": {
                "bsonType": "string",
                "description": "Cryptographic password hash (bcrypt or PBKDF2-SHA256).",
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
