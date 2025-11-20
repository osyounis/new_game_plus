"""
Generates Prolog facts [NOT RULES] from the IGDB game data.

This module reads games.json and creates the knowledge_base.pl with Prolog facts.
"""

import json
from typing import Any


def normalize_string(s: str) -> str:
    """
    Normalize string for Prolog (replace spaces, special characters, etc..)

    Args:
        s: Input string

    Returns:
        Normalized string suitable for Prolog atoms
    """
    # Replaces spaces with underscore, removes special characters
    normalized = s.lower().replace(" ", "_").replace("-", "_")
    # Remove characters that aren't alphanumeric or underscores
    normalized = "".join(c for c in normalized if c.isalnum() or c == "_")

    return normalized


def extract_all_genres(game: dict[str, Any]) -> list[str]:
    """
    Extract all genres from game data.

    Args:
        game: Game dictionary from IGDB

    Returns:
        List of normalized genre names
    """
    genres = []
    if "genres" in game and game["genres"]:
        for genre_obj in game["genres"]:
            if "name" in genre_obj:
                genres.append(normalize_string(genre_obj["name"]))

    return genres if genres else ["unknown"]


def extract_all_platforms(game: dict[str, Any]) -> list[str]:
    """
    Extracts all platforms from game data.

    Args:
        game: Game dictionary from IGDB

    Returns:
        Lists of normalized platform names
    """
    platforms= []
    if "platforms" in game and game["platforms"]:
        for platform_obj in game["platforms"]:
            if "name" in platform_obj:
                platforms.append(normalize_string(platform_obj["name"]))

    return platforms if platforms else ["unknown"]


def generate_prolog_facts(
    input_file: str = "data/games.json",
    output_file: str = "prolog/knowledge_base.pl"
) -> None:
    """
    Generate Prolog facts file from JSON game data.

    Args:
        input_file: Path to games.json file
        output_file: Path to output Prolog file
    """
    # Load game data
    with open(input_file, 'r', encoding="utf-8") as f_obj:
        games = json.load(f_obj)

    # Open output file
    with open(output_file, 'w', encoding="utf-8") as f_obj:
        # Write headers
        f_obj.write("% Game Knowledge Base\n")
        f_obj.write("% Auto-generated from IGDB API data\n")
        f_obj.write("% Format: game(Title, Genre, Platform, Rating)\n")
        f_obj.write("% Note: Games with multiple genres/platforms have multiple facts\n\n")

        # Write facts
        fact_count = 0
        for game in games:
            title = game.get("name", "Unknown")
            rating = int(game.get("total_rating", 0))   # Set to zero is rating not given.

            # Escape single quotes in title
            title_escaped = title.replace("'", "\\'")

            # Extract all genres and platforms
            genres = extract_all_genres(game)
            platforms = extract_all_platforms(game)

            # Create one fact for each combination of genre x platform
            for genre in genres:
                for platform in platforms:
                    fact = f"game('{title_escaped}', {genre}, {platform}, {rating}).\n"
                    f_obj.write(fact)
                    fact_count += 1

    print(f"Generated {fact_count} Prolog facts from {len(games)} games in {output_file}")


def main() -> None:
    """Generate Prolog facts from game data."""
    generate_prolog_facts()


if __name__ == "__main__":
    main()
