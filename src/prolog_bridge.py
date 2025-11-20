"""
Python-Prolog bridge using pyswip.

This module handles communication between Python and SWI-Prolog
"""

from pyswip import Prolog


class PrologBridge:
    """Bridge between Python and Prolog for game recommendations."""


    def __init__(
        self,
        knowledge_base_path: str = "prolog/knowledge_base.pl",
        rules_path: str = "prolog/rules.pl"
    ) -> None:
        """
        Initialize the Prolog bridge and load knowledge base and rules.

        Args:
            knowledge_base_path: Path to Prolog fact file.
            rules_path: Path to Prolog rules file.
        """
        self.prolog = Prolog()

        # Load Prolog files
        try:
            self.prolog.consult(knowledge_base_path)
            self.prolog.consult(rules_path)
            print(f"Loaded Prolog files: {knowledge_base_path}, {rules_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to load Prolog file: {e}") from e


    def get_recommendations_by_genre(
        self,
        game_title: str,
        limit: int = 5
    ) -> list[str]:
        """
        Get game recommendations based on genre matching.

        Args:
            game_title: Title of the game user has provided/played.
            limit: Max number of recommendations. Defaults to 5.

        Returns:
            List of recommended game titles.
        """
        query = f"recommended_by_genre('{game_title}', X)"
        return self._execute_query(query, limit)


    def get_recommendations_by_platform(
        self,
        game_title: str,
        limit: int = 5,
    ) -> list[str]:
        """
        Get game recommendations based on platform matching.

        Args:
            game_title: Title of the game user has provided/played.
            limit: Max number of recommendations. Defaults to 5.

        Returns:
            List of recommended game titles.
        """
        query = f"recommended_by_platform('{game_title}', X)"
        return self._execute_query(query, limit)


    def get_similar_games(
        self,
        game_title: str,
        limit: int = 5
    ) -> list[str]:
        """
        Get similar game recommendations (same genre + similar rating).

        Args:
            game_title: Title of the game user has provided/played.
            limit: Max number of recommendations. Defaults to 5.

        Returns:
            List of recommended game titles.
        """
        query = f"recommend_similar('{game_title}', X)"
        return self._execute_query(query, limit)


    def get_best_matches(
        self,
        game_title: str,
        limit: int = 5
    ) -> list[str]:
        """
        Get best matching recommendations (genre + platform + rating).

        Args:
            game_title: Title of the game user has provided/played.
            limit: Max number of recommendations. Defaults to 5.

        Returns:
            List of recommended game titles.
        """
        query = f"recommend_best_match('{game_title}', X)"
        return self._execute_query(query, limit)


    def _execute_query(self, query: str, limit: int) -> list[str]:
        """
        Execute a Prolog query and return results.

        Args:
            query: Prolog query string.
            limit: Max number of results.

        Returns:
            List of game titles.
        """
        try:
            results = []
            for result in self.prolog.query(query):
                game_title = result.get("X", "")
                if game_title and game_title not in results:
                    results.append(game_title)
                    if len(results) >= limit:
                        break

            return results

        except Exception as e:
            print(f"Error executing Prolog query: {e}")
            return []


def main() -> None:
    """Example usage of PrologBridge."""
    bridge = PrologBridge()

    # Test with a game (replace with an actual game from your knowledge base)
    test_game = "The Witcher 3: Wild Hunt"
    print(f"\Recommendations based on '{test_game}':\n")

    print("By Genre:")
    genre_recs = bridge.get_recommendations_by_genre(test_game, limit=5)
    for i, game in enumerate(genre_recs, 1):
        print(f"  {i}. {game}")

    print("\nBy Platform:")
    platform_recs = bridge.get_recommendations_by_platform(test_game, limit=5)
    for i, game in enumerate(platform_recs, 1):
        print(f"  {i}. {game}")

    print("\nSimilar Games:")
    similar_recs = bridge.get_similar_games(test_game, limit=5)
    for i, game in enumerate(similar_recs, 1):
        print(f"  {i}. {game}")

    print("\nBest Match Games:")
    best_recs = bridge.get_best_matches(test_game, limit=5)
    for i, game in enumerate(best_recs, 1):
        print(f"  {i}. {game}")


if __name__ == "__main__":
    main()
