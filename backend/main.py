"""
MovieVault - Main Interactive Application & Console CLI (main.py).
Provides a unified interactive menu to test, query, and demonstrate all features:
- All 8 Requirements (MongoDB queries and aggregations)
- TMDb External API Cache-Aside integration
- Unified Multi-Database Hub (MongoDB, Apache Cassandra, Dgraph)
"""

import sys
import os
from connect import get_hub, get_mongodb, get_cassandra, get_dgraph, print_database_status


from db.mongodb.schema import setup_schema


def clear_screen() -> None:
    """Clears terminal screen cleanly if in an interactive terminal."""
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    print(r"""
========================================================================
   __  ___           _    _   __            _ _   
  /  |/  /___ _  __ (_)__ | | / /___ ___ __ | | |_ 
 / /|_/ // _ \ |/ // // -_)| |/ // _ `/ // /| |  _/
/_/  /_/ \___/___//_/ \__/ |___/ \_,_/ \_,_/|_|\__| 
             Film Exploration & Review Platform
========================================================================
    """)


def get_input(prompt: str, default: str) -> str:
    """Helper to prompt user with an easily skippable default value."""
    user_val = input(f"{prompt} [Default: '{default}']: ").strip()
    return user_val if user_val else default


def normalize_movie(m: dict) -> dict:
    """Helper to extract common movie fields regardless of schema version."""
    title = m.get("title") or m.get("movie_title", "Unknown")
    year = m.get("release_year", "N/A")
    rating = m.get("rating") if m.get("rating") is not None else m.get("avg_rating", "N/A")
    impact = m.get("impact_score", "N/A")
    return {"title": title, "year": year, "rating": rating, "impact": impact}


# ==============================================================================
# MENU ACTIONS
# ==============================================================================

def action_req1(db) -> None:
    print("\n--- REQ 1: Movies by Title, Decade & Language (Impact Sorted) ---")
    title = get_input("Movie title contains", "The")
    min_dec = int(get_input("Min Decade", "1990"))
    max_dec = int(get_input("Max Decade", "2020"))
    lang = get_input("Language code", "en")

    # res = get_movies_by_title_decade_language(
    #     db, 
    #     title_query=title, 
    #     min_decade=min_dec,
    #     max_decade=max_dec, 
    #     language=lang
    # )


def action_req2(db) -> None:
    print("\n--- REQ 2: Movies by Genre and Country (and optional Director) ---")
    genre = get_input("Genre", "Drama")
    country = get_input("Country", "USA")
    director = input("Director name (optional, press Enter to omit): ").strip() or None

    # res = get_movies_by_genre_and_country(
    #     db, 
    #     genre=genre, 
    #     country=country,
    #     director=director
    # )


def action_req3(db) -> None:
    print("\n--- REQ 3: Movies by Rating Threshold, Director, and Decade ---")
    min_rating = float(get_input("Minimum Rating (0.0 to 5.0)", "4.5"))
    director = get_input("Director Name", "Christopher Nolan")
    decade = int(get_input("Decade", "2010"))

    # res = get_movies_by_rating_director_decade(
    #     db, 
    #     min_rating=min_rating, 
    #     director=director, 
    #     min_decade=decade, 
    #     max_decade=decade
    # )


def action_req4(db) -> None:
    print("\n--- REQ 4: Movies by Keywords in Synopsis ---")
    keywords = get_input("Keywords to search in synopsis", "dreams")

    # res = get_movies_by_synopsis_keywords(
    #     db, 
    #     keywords=keywords
    # )


def action_req5(db) -> None:
    print("\n--- REQ 5: Reviews by Keywords (Sorted by Likes & Comments) ---")
    movie_title = get_input("Filter by Movie Title", "Inception")
    keywords = get_input("Keywords in review text", "dreams")

    # res = get_reviews_by_keywords(
    #     db, 
    #     keywords=keywords, 
    #     movie_title=movie_title
    # )


def action_req6(db) -> None:
    print("\n--- REQ 6: Movies by Actor and/or Director ---")
    actor = get_input("Actor Name", "Leonardo DiCaprio")
    director = get_input("Director Name", "Quentin Tarantino")
    mode = get_input("Match Mode ('OR' or 'AND')", "OR")

    # res = get_movies_by_actor_and_director(
    #     db, 
    #     actor=actor, 
    #     director=director, 
    #     match_mode=mode
    # )


def action_req7(db) -> None:
    print("\n--- REQ 7: Actor Career and Impact Aggregation ---")
    actor = get_input("Actor Name", "Leonardo DiCaprio")

    # stats = get_actor_impact_aggregation(
    #     db, 
    #     actor_identifier=actor
    # )


def action_req8(db) -> None:
    print("\n--- REQ 8: User Historical Profile & Wrapped Aggregation ---")
    username = get_input("Username", "cinephile_sam")

    # stats = get_user_statistics_aggregation(
    #     db, 
    #     identifier=username
    # )


def action_tmdb_integration(db) -> None:
    pass


def action_database_diagnostics() -> None:
    pass


def action_initialize_database(db) -> None:
    print("\n--- Initializing MongoDB Schema and Loading Seed Data ---")
    setup_schema(db)
    print("Database schema initialized successfully!")


# ==============================================================================
# MAIN MENU LOOP
# ==============================================================================

def main() -> None:
    hub = get_hub()
    db = hub.get_mongodb()

    while True:
        print_banner()
        print("UNIFIED PLATFORM MENU:")
        print("  1.  [Req 1] Search movies by Title, Decade & Language (Impact sorted)")
        print("  2.  [Req 2] Search movies by Genre & Country (and Director)")
        print("  3.  [Req 3] Search movies by Rating threshold, Director & Decade")
        print("  4.  [Req 4] Search movies by Keywords in Synopsis")
        print("  5.  [Req 5] Search reviews by Keywords (Sorted by Likes & Comments)")
        print("  6.  [Req 6] Search movies by Actor and/or Director")
        print("  7.  [Req 7] Actor Career & Impact Aggregation Pipeline")
        print("  8.  [Req 8] User Historical Statistics (Spotify Wrapped Style)")
        print("  ----------------------------------------------------------------")
        print("  9.  [TMDb] Search TMDb and Cache-Aside into MongoDB")
        print("  10. [Diagnostics] Check Unified Databases (MongoDB, Cassandra, Dgraph)")
        print("  11. [Setup] Re-initialize Schema & Seed Sample Data")
        print("  0.  Exit")
        print("=" * 72)

        choice = input("Select an option [0-11]: ").strip()

        if choice == "0":
            print("\nShutting down unified database connections...")
            hub.close_all()
            print("Goodbye!\n")
            sys.exit(0)

        try:
            if choice == "1":
                action_req1(db)
            elif choice == "2":
                action_req2(db)
            elif choice == "3":
                action_req3(db)
            elif choice == "4":
                action_req4(db)
            elif choice == "5":
                action_req5(db)
            elif choice == "6":
                action_req6(db)
            elif choice == "7":
                action_req7(db)
            elif choice == "8":
                action_req8(db)
            elif choice == "9":
                action_tmdb_integration(db)
            elif choice == "10":
                action_database_diagnostics()
            elif choice == "11":
                action_initialize_database(db)
            else:
                print("\n[!] Invalid option. Please choose between 0 and 11.")
        except Exception as e:
            print(f"\n[ERROR occurred during execution]: {e}")

        input("\nPress [Enter] to return to the main menu...")
        clear_screen()


if __name__ == "__main__":
    main()
