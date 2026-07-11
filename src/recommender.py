import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


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
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for a user (placeholder slice, no scoring yet)."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explains why a specific song was recommended to the user (placeholder)."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    """Loads song data from a CSV file into a list of dictionaries."""
    songs = []
    with open(csv_path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs


# --- Weight-shift experiment scaffolding -----------------------------------
# Original hardcoded point values, kept here so the change is easy to revert.
ORIGINAL_WEIGHTS = {
    "genre": 2.0,
    "mood": 1.0,
    "energy_max": 2.0,
    "acoustic": 1.0,
}

# --- EXPERIMENTAL CHANGE: Weight Shift (energy doubled, genre halved) ------
DEFAULT_WEIGHTS = {
    "genre": 1.0,        # was 2.0 (halved)
    "mood": 1.0,         # unchanged
    "energy_max": 4.0,   # was 2.0 (doubled)
    "acoustic": 1.0,     # unchanged
}
# NOTE: max possible score changed from 6.0 -> 7.0. See verify_weight_shift.py
# for the check that confirms this and what it means for any score thresholds.
# To revert: DEFAULT_WEIGHTS = ORIGINAL_WEIGHTS.copy()
# -----------------------------------------------------------------------------


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Scores a song against user preferences and returns the score with reasons."""
    if weights is None:
        weights = DEFAULT_WEIGHTS

    score = 0.0
    reasons = []

    # Genre match
    if song["genre"] == user_prefs["favorite_genre"]:
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.2f})")

    # Mood match
    if song["mood"] == user_prefs["favorite_mood"]:
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.2f})")

    # Energy similarity: linear falloff from energy_max at diff=0 to 0 at diff=1.0
    energy_diff = abs(song["energy"] - user_prefs["target_energy"])
    energy_max = weights["energy_max"]
    energy_points = max(0.0, energy_max * (1 - energy_diff))
    if energy_points > 0:
        score += energy_points
        reasons.append(f"energy closeness (+{round(energy_points, 2)})")

    # Bonus: acousticness preference
    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) > 0.6:
        score += weights["acoustic"]
        reasons.append(f"high acousticness (+{weights['acoustic']:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Optional[Dict] = None) -> List[Tuple[Dict, float, str]]:
    """Scores every song, ranks them, and returns the top k recommendations."""
    def build_result(song):
        """Scores a song and packages it with its explanation into a result tuple."""
        score, reasons = score_song(user_prefs, song, weights=weights)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        return (song, score, explanation)

    scored = [build_result(song) for song in songs]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
