"""
Main application for game recommendation system.

This is the entry point that ties together the IGDB API, bridge, and user
interface.
"""

import argparse
from prolog_bridge import PrologBridge


def display_recommendations(
    game_title: str,
    recommendations: dict[str, list[str]]
) -> None:
    """
    Display recommendations to the user.

    Args:
        game_title: The game the user provided/played.
        recommendations: Dictionary of recommendation types and game lists.
    """
    print("\n" + "=" * 60)
    print(f"Recommendations based on: {game_title}")
    print("=" * 60 + "\n")

    for rec_type, games in recommendations.items():
        print(f"{rec_type}:")
        if games:
            for i, game in enumerate(games, 1):
                print(f"  {i}. {game}")
        else:
            print("  No recommendations found.")
        print()


def get_recommendations(game_title: str, limit: int = 5) -> dict[str, list[str]]:
    """
    Get all types of recommendations for a game.

    Args:
        game_title: Title of game the user provided/played.
        limit: MAx number of recommendations per category. Defaults to 5.

    Returns:
        Dictionary with recommendation types as keys and game lists as values.
    """
    bridge = PrologBridge()

    recommendations = {
        "Similar Games (Genre + Rating)": bridge.get_similar_games(game_title, limit),
        "Same Genre": bridge.get_recommendations_by_genre(game_title, limit),
        "Same Platform": bridge.get_recommendations_by_platform(game_title, limit),
        "Best Matches (Genre + Platform + Rating)": bridge.get_best_matches(game_title, limit),
    }

    return recommendations


def main() -> None:
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Get game recommendations based on a game you have played."
    )
    parser.add_argument(
        "--game",
        type=str,
        help="Title of the game you have played (must match exactly)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of recommendations per category (default: 5)",
    )

    args = parser.parse_args()

    # If no game specified, prompt user
    if not args.game:
        print("\nGame Recommendation System")
        print("-" * 60)
        game_title = input("Enter a game you've played: ").strip()
    else:
        game_title = args.game

    if not game_title:
        print("Error: No game title provided")
        return

    # Get and display recommendations
    try:
        recommendations = get_recommendations(game_title, args.limit)
        display_recommendations(game_title, recommendations)

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure:")
        print("  1. The game title matches exactly (case-sensitive)")
        print("  2. The game exists in the knowledge base")
        print("  3. SWI-Prolog is installed and accessible")


if __name__ == "__main__":
    main()
