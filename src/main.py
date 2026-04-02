"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from recommender import load_songs, recommend_songs


def main() -> None:
    """
    Main entry point for the music recommender.
    Loads songs and runs recommendations for a default user profile.
    """
    # Determine the correct path to songs.csv
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    csv_path = os.path.join(project_root, "data", "songs.csv")

    # Load the song catalog
    songs = load_songs(csv_path)
    print(f"✓ Loaded {len(songs)} songs from catalog\n")

    # Default user profile: pop/happy vibe
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_valence": 0.8,
        "likes_acoustic": False
    }

    print("=" * 70)
    print(f"USER PROFILE: {user_prefs['favorite_genre'].upper()} / {user_prefs['favorite_mood'].upper()}")
    print(f"Target Energy: {user_prefs['target_energy']:.1f}  |  Target Valence: {user_prefs['target_valence']:.1f}")
    print("=" * 70)

    # Get top 5 recommendations
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTOP 5 RECOMMENDATIONS:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{rank}. {song['title']:35} | {song['artist']:20} | Score: {score:.2f}")
        print(f"   Genre: {song['genre']:12} | Mood: {song['mood']:15} | Energy: {song['energy']:.2f}")
        print(f"   → {explanation}")
        print()


if __name__ == "__main__":
    main()
