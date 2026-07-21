import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the song catalog this recommender ranks against."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Return the top k songs for the given user, highest score first.

        Reuses the shared score_song() judge so the OOP path and the
        functional path (recommend_songs) rank songs identically. The
        dataclasses are converted to dicts because score_song() reads
        preferences and attributes by key.
        """
        user_prefs = asdict(user)
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _reasons = score_song(user_prefs, asdict(song))
            scored.append((song, score))

        # Sort by score (index 1), highest first.
        scored.sort(key=lambda item: item[1], reverse=True)

        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Return a human-readable sentence explaining why a song fits the user.

        Builds the sentence from the same reasons score_song() collects, so
        the explanation always matches the score that ranked the song.
        """
        _score, reasons = score_song(asdict(user), asdict(song))
        if not reasons:
            return f"'{song.title}' has no strong match with your preferences."
        return f"'{song.title}' was recommended because it " + "; ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns are converted from strings to the right type:
    - id, tempo_bpm            -> int
    - energy, valence,
      danceability, acousticness -> float
    Text columns (title, artist, genre, mood) are left as strings.

    Required by src/main.py
    """
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            for field in int_fields:
                song[field] = int(song[field])
            for field in float_fields:
                song[field] = float(song[field])
            songs.append(song)

    return songs

# Scoring weights (see README "How The System Works").
# Priority ladder: mood > energy > genre > acoustic.
# Change any of these to run experiments and re-rank.
W_MOOD = 2.0
W_ENERGY = 1.5
W_GENRE = 1.0
W_ACOUSTIC = 0.5


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Recipe (weighted sum, each term on a 0->1 scale before weighting):
        score = W_MOOD    * mood_match       # 1 if moods match, else 0
              + W_ENERGY  * energy_closeness # 1 - |song energy - target|
              + W_GENRE   * genre_match      # 1 if genres match, else 0
              + W_ACOUSTIC* acoustic_fit     # acousticness if user likes
                                             # acoustic, else 1 - acousticness
    Max possible score = 5.0.

    Required by recommend_songs() and src/main.py
    """
    # Read preferences, supporting both key styles used in main.py:
    # the starter dict ("mood"/"energy"/"genre") and the listener dicts
    # ("favorite_mood"/"target_energy"/"favorite_genre"/"likes_acoustic").
    fav_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))
    fav_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    likes_acoustic = user_prefs.get("likes_acoustic")

    score = 0.0
    reasons: List[str] = []

    # 1. Mood: exact-match switch.
    if fav_mood is not None and song["mood"] == fav_mood:
        score += W_MOOD
        reasons.append(f"matches your favorite mood ({fav_mood})")

    # 2. Energy: closeness to the target (clamped to [0, 1]).
    if target_energy is not None:
        energy_closeness = max(0.0, 1.0 - abs(song["energy"] - target_energy))
        score += W_ENERGY * energy_closeness
        reasons.append(
            f"energy {song['energy']:.2f} is close to your target "
            f"{target_energy:.2f}"
        )

    # 3. Genre: exact-match switch.
    if fav_genre is not None and song["genre"] == fav_genre:
        score += W_GENRE
        reasons.append(f"matches your favorite genre ({fav_genre})")

    # 4. Acoustic: reward high acousticness if the user likes acoustic,
    #    otherwise reward low acousticness.
    if likes_acoustic is not None:
        acoustic_fit = (
            song["acousticness"] if likes_acoustic else 1.0 - song["acousticness"]
        )
        score += W_ACOUSTIC * acoustic_fit
        preference = "acoustic" if likes_acoustic else "non-acoustic"
        reasons.append(f"fits your {preference} preference")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks the catalog for a user and returns the top k recommendations.

    Steps:
    1. Score every song with score_song() (the judge).
    2. Sort all songs by score, highest first.
    3. Return the top k as (song_dict, score, explanation) tuples,
       where explanation is a human-readable sentence built from the
       reasons score_song() gave.

    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))

    # Sort by score (index 1), highest first.
    scored.sort(key=lambda item: item[1], reverse=True)

    return scored[:k]
