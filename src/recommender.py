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
    Mirrors the scoring formula used by score_song() below so the class-based
    and functional APIs stay in sync.
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Return (score, reasons) for a single song against a user profile."""
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood == user.favorite_mood:
            score += 1.5
            reasons.append("mood match (+1.5)")

        energy_similarity = 1.0 - abs(song.energy - user.target_energy)
        score += energy_similarity
        reasons.append(f"energy similarity ({energy_similarity:.2f})")

        if user.likes_acoustic and song.acousticness > 0.7:
            score += 0.5
            reasons.append("acousticness match (+0.5)")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs, ranked by score descending."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        # Stable sort preserves input order on ties.
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Human-readable explanation of why a song was recommended."""
        score, reasons = self._score(user, song)
        reason_text = ". ".join(reasons) if reasons else "no matching signals"
        return f"Score {score:.2f} - {reason_text}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Converts numerical columns (energy, tempo_bpm, valence, danceability, acousticness) to floats.
    Returns a list of song dictionaries.
    """
    import csv
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numerical columns to floats
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            row['id'] = int(row['id'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song based on user preferences.

    Args:
        user_prefs: User profile dict with favorite_genre, favorite_mood, target_energy,
                   target_valence, likes_acoustic
        song: Song dict with genre, mood, energy, valence, acousticness

    Returns:
        Tuple of (total_score: float, reasons: List[str])
        Reasons explain which features matched and contributed to the score.

    Algorithm:
        score = (genre_match × 2.0)
              + (mood_match × 1.5)
              + (energy_similarity × 1.0)
              + (valence_similarity × 0.5)
              + (acousticness_bonus)
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0 points
    if song['genre'] == user_prefs['favorite_genre']:
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match: +1.5 points
    if song['mood'] == user_prefs['favorite_mood']:
        score += 1.5
        reasons.append(f"mood match (+1.5)")

    # Energy similarity: 1.0 - abs(target - actual), scaled by 1.0
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_similarity = 1.0 - energy_diff
    energy_score = energy_similarity * 1.0
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:.2f})")

    # Valence similarity: 1.0 - abs(target - actual), scaled by 0.5
    target_valence = user_prefs.get('target_valence', 0.5)  # Default to neutral
    valence_diff = abs(song['valence'] - target_valence)
    valence_similarity = 1.0 - valence_diff
    valence_score = valence_similarity * 0.5
    score += valence_score
    reasons.append(f"valence similarity ({valence_score:.2f})")

    # Acousticness bonus: +0.5 if user likes acoustic AND song is acoustic (>0.7)
    if user_prefs.get('likes_acoustic', False) and song['acousticness'] > 0.7:
        score += 0.5
        reasons.append(f"acousticness match (+0.5)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores all songs and returns top K recommendations with explanations.

    Args:
        user_prefs: User profile dict with favorite_genre, favorite_mood, target_energy,
                   target_valence, likes_acoustic
        songs: List of song dicts to score and rank
        k: Number of top recommendations to return (default: 5)

    Returns:
        List of tuples: (song_dict, score: float, explanation: str)
        Sorted by score descending. Ties broken by input order (deterministic).

    Algorithm (Pythonic approach using sorted()):
        1. Loop through all songs
        2. For each song, judge it using score_song() function
        3. Build (song, score, explanation) tuples
        4. Use sorted() to create new sorted list (highest score first)
        5. Slice [:k] to return top K results
    """
    # Judge every song in the catalog using score_song() as the judge
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ". ".join(reasons)
        scored_songs.append((song, score, explanation))

    # sorted() returns a new sorted list (more Pythonic than .sort())
    # Ties are broken by input order because Python's sort is stable
    return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]
