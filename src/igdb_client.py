"""
IGDB API client for getting game data.

This module handles authentication and getting data from the IGDB API.
"""

import os
import json

from typing import Any

import requests
from dotenv import load_dotenv


class IGDBClient:
    """Client for interacting with the IGDB API."""

    def __init__(self) -> None:
        """
        Initialize the IGDB client and authenticate.
        """
        load_dotenv()
        self.client_id = os.getenv("IGDB_CLIENT_ID")
        self.client_secret = os.getenv("IGDB_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError("IGDB_CLIENT_ID and IGDB_CLIENT_SECRET must be set in .env file")

        self.access_token = self._get_access_token()
        self.base_url = "https://api.igdb.com/v4"
        self.headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }


    def _get_access_token(self) -> str:
        """
        Get OAuth access token from Twitch. Twitch is needed to get to the IGDB.

        Returns:
            Access token in a string

        Raises:
            requests.RequestException: If authentication fails
        """
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        response = requests.post(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        return data["access_token"]


    def fetch_games(self, query: str, limit: int = 50) -> list[dict[str, Any]]:
        """
        Gets games form IGDB API using custom query.

        Args:
            query: IGDB API query string
            limit: Max number of games to get. Defaults to 50.

        Returns:
            List of games in dictionaries
            
        Raise: 
            requests.RequestException: If API request fails
        """
        url = f"{self.base_url}/games"

        # Ensure limit is in the query [Safety measure]
        if "limit" not in query:
            query = query.strip()
            # Add limit without creating double semicolons
            if not query.endswith(';'):
                query += ';'
            query += f" limit {limit};"

        response = requests.post(url, headers=self.headers, data=query, timeout=30)
        response.raise_for_status()

        return response.json()


    def save_games_to_json(
            self,
            games: list[dict[str, Any]],
            filename: str = "data/games.json"
        ) -> None:
        """
        Save game data to JSON file.

        Args:
            game: List of games in dictionaries
            filename: Output file path. Defaults to "data/games.json".
        """
        with open(filename, "w", encoding="utf-8") as f_obj:
            json.dump(games, f_obj, indent=2, ensure_ascii=False)

        print(f"Saved {len(games)} games to {filename}")


def main() -> None:
    """Example of how to use IGDBClient."""
    client = IGDBClient()

    # Fields: name, total_rating, slug, platforms, genres, publishers
    # Sorted by highest rated games first
    query = """
    fields name, total_rating, slug, platforms.name, genres.name, version_parent;
    where total_rating_count >= 100 & total_rating != null & version_parent = null & game_type = 0;
    sort total_rating desc;
    """

    print("Getting games form IGDB...")
    games = client.fetch_games(query)       # Uses default limit of 50 games

    print(f"Got {len(games)} games")

    # Save to JSON
    client.save_games_to_json(games)

    print("Job's Done!")


if __name__ == "__main__":
    main()
