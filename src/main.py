"""
Command line runner for the Music Recommender Simulation.

Runs the recommender across three diverse user profiles plus one
"adversarial" contradictory profile used as an edge case. For each
profile it prints the top 5 ranked songs with scores and explanations.
"""

import os
from recommender import load_songs, recommend_songs


USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.55,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "target_valence": 0.55,
        "likes_acoustic": False,
    },
    # Adversarial / edge case: asks for gym-level energy with a sad mood and
    # an obscure genre. Tests whether the scorer can still rank reasonably
    # when the profile's fields pull in different directions.
    "Contradictory (High Energy + Melancholic)": {
        "favorite_genre": "indie",
        "favorite_mood": "melancholic",
        "target_energy": 0.9,
        "target_valence": 0.4,
        "likes_acoustic": False,
    },
}


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    print("=" * 70)
    print(f"USER PROFILE: {profile_name}")
    print(
        f"Prefs: genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, "
        f"target_energy={user_prefs['target_energy']:.2f}, "
        f"target_valence={user_prefs['target_valence']:.2f}, "
        f"likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("=" * 70)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{rank}. {song['title']:30} | {song['artist']:20} | Score: {score:.2f}")
        print(
            f"   Genre: {song['genre']:12} | Mood: {song['mood']:15} | "
            f"Energy: {song['energy']:.2f}"
        )
        print(f"   Because: {explanation}")
        print()


def main() -> None:
    """Load the catalog and print recommendations for every user profile."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    csv_path = os.path.join(project_root, "data", "songs.csv")

    songs = load_songs(csv_path)
    print(f"Loaded {len(songs)} songs from catalog\n")

    for profile_name, prefs in USER_PROFILES.items():
        print_recommendations(profile_name, prefs, songs)


if __name__ == "__main__":
    main()
