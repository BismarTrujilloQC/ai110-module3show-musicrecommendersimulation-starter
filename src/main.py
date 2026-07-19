"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # Works when run as a module from the repo root: python -m src.main
    from src.recommender import load_songs, recommend_songs
except ImportError:
    # Works when run directly from inside src/: python main.py
    from recommender import load_songs, recommend_songs

MAX_SCORE = 5.0  # See score_song(): W_MOOD + W_ENERGY + W_GENRE + W_ACOUSTIC.


def print_recommendations(recommendations) -> None:
    """Render recommendations as a clean, readable terminal layout."""
    width = 60
    print()
    print("=" * width)
    print("  TOP RECOMMENDATIONS".ljust(width))
    print("=" * width)

    for rank, rec in enumerate(recommendations, start=1):
        # Each item is (song, score, explanation), where explanation is the
        # reasons from score_song() joined with "; ".
        song, score, explanation = rec
        reasons = explanation.split("; ") if explanation else []

        print()
        print(f"  {rank}. {song['title']}  -  {song['artist']}")
        print(f"     Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("     Why we picked it:")
        for reason in reasons:
            print(f"       * {reason}")

    print()
    print("=" * width)
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile.
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Extra example profiles (not used yet — swap into recommend_songs() to try).
    gym_listener = {
        "favorite_genre": "pop",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "likes_acoustic": False,
    }
    study_listener = {
        "favorite_genre": "lofi",
        "favorite_mood": "focused",
        "target_energy": 0.38,
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
