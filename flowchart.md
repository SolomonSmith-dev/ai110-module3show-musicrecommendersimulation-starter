# Music Recommender Data Flow

```mermaid
flowchart TD
    A["User Profile<br/>(genre, mood, energy, valence, acoustic)"]
    B["Load songs.csv<br/>(20 songs)"]
    
    C["For each song:"]
    D["Calculate genre_match<br/>Calculate mood_match<br/>Calculate energy_similarity<br/>Calculate valence_similarity<br/>Calculate acousticness_bonus"]
    E["Compute total_score"]
    F["Store song + score tuple"]
    
    G["Rank all songs by score<br/>Descending order"]
    H["Break ties deterministically<br/>by input order"]
    I["Return Top K songs<br/>with explanations"]
    J["Output Recommendations"]
    
    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    F -->|repeat for next song| C
    F -->|all songs scored| G
    G --> H
    H --> I
    I --> J
```

## Process Steps

1. **Input**: User profile dict + songs CSV loaded
2. **Scoring Loop**: For each of 20 songs:
   - Compare genre/mood (binary match: 0 or 1)
   - Calculate energy_similarity (1.0 - abs difference)
   - Calculate valence_similarity (1.0 - abs difference)
   - Add acousticness_bonus if user prefers acoustic AND song is acoustic
   - Store (song, total_score)
3. **Ranking**: Sort all scored songs by total_score descending
4. **Tie-Breaking**: Maintain input order for same scores (deterministic)
5. **Output**: Return top K songs with explanations showing matched features
