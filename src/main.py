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


USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.88,
        "likes_acoustic": False,
    },
}


# Three profiles built to "trick" score_song() and expose its blind spots.

ADVERSARIAL_PROFILES = {
    # Conflict: asks for high energy but a low-energy mood. Mood (weight 2.0)
    # wins, so a near-silent track outranks the energetic songs the user wanted.
    "Conflicting Energy vs Mood": {
        "favorite_genre": "classical",
        "favorite_mood": "melancholic",
        "target_energy": 0.95,
        "likes_acoustic": False,
    },
    # Hidden correlation: acoustic songs are all low-energy in this catalog, so
    # "acoustic + high energy" can't co-exist. The winner is labeled acoustic
    # while actually being one of the least acoustic tracks.
    "Acoustic Lover, High Energy": {
        "favorite_genre": "edm",
        "favorite_mood": "euphoric",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
    # Ghost preferences: genre/mood don't exist in the catalog, so those terms
    # silently score 0 and ranking collapses to energy + acoustic only.
    "Ghost Preferences": {
        "favorite_genre": "kpop",
        "favorite_mood": "grumpy",
        "target_energy": 0.50,
        "likes_acoustic": False,
    },
}


def print_recommendations(recommendations, title: str = "TOP RECOMMENDATIONS") -> None:
    """Render recommendations as a clean, readable terminal layout."""
    width = 60
    print()
    print("=" * width)
    print(f"  {title}".ljust(width))
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

    # Run the simulation for each distinct listener profile.
    for profile_name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(recommendations, title=f"{profile_name.upper()} PICKS")

    # Then run the adversarial / edge-case profiles to stress-test the scorer.
    for profile_name, user_prefs in ADVERSARIAL_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(recommendations, title=f"[ADVERSARIAL] {profile_name.upper()}")


if __name__ == "__main__":
    main()
