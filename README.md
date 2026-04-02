# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

**What We're Building:**
A content-based recommender. Spotify uses collaborative filtering (what other users like) + content-based (song attributes). We're doing the second part: match songs to what a user explicitly says they want. It's transparent, works immediately on new songs, no cold-start. Downside: only finds similar stuff, no serendipity. But it works.

**The Scoring Formula:**
```
score = (genre_match × 2.0) + (mood_match × 1.5) + energy_similarity + (valence_similarity × 0.5)
```

Genre and mood are binary matches (worth more because they're foundational filters). Energy and valence use proximity: `1.0 - abs(user_target - song_value)`. This rewards songs close to what you want, not extremes.

**Song Features:**
- `genre`: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, country, electronic, r&b, metal, folk, k-pop, reggae, classical
- `mood`: happy, chill, intense, relaxed, moody, focused, melancholic, nostalgic, energetic, sensual, aggressive, peaceful, laid-back, upbeat, serene
- `energy` (0.0–1.0): how intense/lively
- `valence` (0.0–1.0): how bright/optimistic vs. dark/sad
- `danceability` (0.0–1.0): how dance-friendly
- `acousticness` (0.0–1.0): acoustic vs. synth

**User Profile Stores:**
- `favorite_genre` (string)
- `favorite_mood` (string)
- `target_energy` (0.0–1.0)
- `target_valence` (0.0–1.0)
- `likes_acoustic` (boolean)

**Algorithm Recipe (Finalized):**

For each song, calculate:
```
score = (genre_match × 2.0) 
      + (mood_match × 1.5) 
      + (energy_similarity × 1.0)
      + (valence_similarity × 0.5)
      + (acousticness_bonus)
```

Where:
- `genre_match` = 1.0 if genres match, else 0.0
- `mood_match` = 1.0 if moods match, else 0.0
- `energy_similarity` = 1.0 - abs(song.energy - user.target_energy)
- `valence_similarity` = 1.0 - abs(song.valence - user.target_valence)
- `acousticness_bonus` = 0.5 if user.likes_acoustic AND song.acousticness > 0.7, else 0.0

Then rank all songs by score (descending). For ties, maintain input order.

**Expected Biases:**
- **Genre over-prioritization**: Genre weight (2.0) is highest. A user seeking "hip-hop" won't see great "indie" songs even if mood/energy are perfect matches.
- **Filter bubble**: System only recommends similar songs. Won't expose users to unexpected artists or moods outside their stated preferences.
- **Mood label bias**: Categorical mood depends on subjective labeling. Two "introspective" songs might feel very different emotionally.
- **Small catalog**: With only 20 songs, some genre/mood combos are underrepresented (no "happy metal" songs). Real systems have 50M+ songs.
- **No user history**: System doesn't learn; same profile always gets same results. Real Spotify adapts based on what you actually listen to.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python src/main.py
   ```

### CLI Verification (Sample Output)

Running with default pop/happy user profile:

```
✓ Loaded 20 songs from catalog

======================================================================
USER PROFILE: POP / HAPPY
Target Energy: 0.8  |  Target Valence: 0.8
======================================================================

TOP 5 RECOMMENDATIONS:

1. Sunrise City                        | Neon Echo            | Score: 4.96
   Genre: pop          | Mood: happy           | Energy: 0.82
   → genre match (+2.0). mood match (+1.5). energy similarity (0.98). valence similarity (0.48)

2. Gym Hero                            | Max Pulse            | Score: 3.35
   Genre: pop          | Mood: intense         | Energy: 0.93
   → genre match (+2.0). energy similarity (0.87). valence similarity (0.48)

3. Rooftop Lights                      | Indigo Parade        | Score: 2.96
   Genre: indie pop    | Mood: happy           | Energy: 0.76
   → mood match (+1.5). energy similarity (0.96). valence similarity (0.49)

4. Everlong                            | Foo Fighters         | Score: 1.39
   Genre: rock         | Mood: intense         | Energy: 0.85
   → energy similarity (0.95). valence similarity (0.44)

5. PRIDE.                              | Kendrick Lamar       | Score: 1.34
   Genre: hip-hop      | Mood: intense         | Energy: 0.79
   → energy similarity (0.99). valence similarity (0.35)
```

**Verification:** Top result is "Sunrise City" (4.96 points) — perfect match for pop/happy profile (genre + mood + energy match).

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

