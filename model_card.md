# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0** - a small content-based music recommender.

---

## 2. Intended Use

VibeFinder is a classroom simulation. It takes a short "taste profile"
(favorite genre, favorite mood, target energy, target valence, whether
the user likes acoustic music) and returns the top 5 songs from a 20-song
catalog, along with a reason for each recommendation.

It is **not** a product. It is a teaching model that makes the scoring
logic of a real recommender visible. It assumes:

- The user can state their preferences in clean categorical terms.
- The catalog's labels (genre, mood) are reasonably accurate.
- The user wants songs similar to their stated preferences, not diverse
  or novel ones.

Real users, real catalogs, and real taste do not satisfy these
assumptions, so VibeFinder should not be used for anything with stakes.

---

## 3. How the Model Works

VibeFinder treats recommendation as scoring-and-ranking. For each song
in the catalog, it computes a single number:

- **Genre match (+2.0):** If the song's genre equals the user's favorite
  genre, add 2 points. This is the single biggest signal.
- **Mood match (+1.5):** If the song's mood label equals the user's
  favorite mood, add 1.5 points.
- **Energy similarity (+0 to +1.0):** Songs whose energy is close to the
  user's target energy score higher; a perfect match adds 1.0, a total
  mismatch adds 0.
- **Valence similarity (+0 to +0.5):** Same idea for valence (how
  upbeat vs. dark the song feels), worth half as much as energy.
- **Acoustic bonus (+0.5):** If the user said they like acoustic music
  and the song is more than 70% acoustic, add 0.5.

After every song has a score, the model sorts them and returns the top 5.
Ties are broken by input order. For each recommendation it also returns
a list of the specific points that were awarded, so the user can see
why the song made the list.

I changed one thing from the starter logic: I added the acoustic bonus
and valence similarity on top of genre, mood, and energy. The starter
formula was simpler; these two features give the scorer more to work
with and let users with a preference for acoustic music actually signal
that preference.

---

## 4. Data

The catalog is `data/songs.csv`, which I expanded from the 10 starter
songs to 20 to get more coverage. Each row has:

- `id`, `title`, `artist`
- Categorical: `genre`, `mood`
- Numeric (0.0-1.0): `energy`, `valence`, `danceability`, `acousticness`
- Numeric (BPM): `tempo_bpm`

Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop,
hip-hop, alternative, trip-hop, indie, electronic, indie rock, alt
country. Moods include happy, chill, intense, relaxed, moody, focused,
introspective, melancholic, dark.

What is missing: entire regional styles (K-pop, reggaeton, Afrobeat,
classical, country, metal), non-English music, and a huge swath of
"positive but not happy" moods like euphoric, triumphant, or wistful.
The catalog mostly reflects the taste of a single person in 2024 with a
lean toward introspective / alternative music. That bias is baked in
before any scoring happens.

---

## 5. Strengths

- **Transparency.** Every recommendation comes with a list of the exact
  reasons that contributed to its score. Someone auditing the system
  can see whether the genre, mood, or energy drove a result.
- **Deterministic.** Same inputs always give the same outputs. That
  makes it easy to test and easy to reason about.
- **No cold-start problem.** The system works on any new song the
  moment it's added to the CSV, because it does not rely on user
  listening history.
- **Simple scoring shape.** Scores are bounded, the weights are in one
  place, and the behavior can be tuned by changing four numbers. That
  makes the model easy to teach and easy to change.
- **Good on clean profiles.** The three non-adversarial profiles
  (pop/happy, lofi/chill, rock/intense) each produced a top result that
  I would personally rank as a reasonable top pick from the catalog.

---

## 6. Limitations and Bias

- **Genre dominance.** Genre is worth 2.0 points - more than any other
  single signal. A user who cares more about mood than genre still ends
  up with genre-heavy results. If the product goal were to surface
  cross-genre mood matches (chill jazz for a chill lofi listener), the
  current weights would fight against it.
- **Categorical override on numeric signals.** When a profile is
  internally contradictory (e.g., energy 0.9 + mood "melancholic"),
  the categorical matches win and the rankings ignore how different the
  actual song energy is from the target. The "Contradictory" profile in
  main.py demonstrates this: the #1 pick is a slow Bon Iver track, not
  a high-energy track.
- **Dataset skew.** With only 20 songs, some genre/mood combinations
  simply have no entries. A user asking for "happy metal" gets nothing
  that could reasonably be called that.
- **No diversity.** The top 5 can include three songs by the same
  artist. Real systems would apply a diversity penalty.
- **Label quality.** The mood column is one word. Real moods are
  multi-dimensional, and two songs with the same label can feel very
  different.
- **Single-user assumption.** No concept of history, feedback, or
  context (time of day, activity, location).

Where this could be unfair in a real product: users whose tastes don't
match any dominant genre in the catalog get consistently worse
recommendations than users who match a well-populated genre. That
inequality grows larger as the catalog grows - not smaller.

---

## 7. Evaluation

I evaluated VibeFinder in three ways:

1. **Profile coverage.** Four user profiles: High-Energy Pop, Chill
   Lofi, Deep Intense Rock, and a deliberately contradictory
   High-Energy Melancholic Indie. For each I checked whether the top
   result was a song I would actually pick by hand. Three of four felt
   right. The contradictory profile produced a result that was
   technically correct under the scoring rule but clearly wrong
   musically.
2. **Sensitivity experiment.** I doubled the energy weight and re-ran
   the contradictory profile. Holocene (slow indie) fell from #1 to #3
   and Storm Runner (fast rock, no categorical match) rose to #1. This
   shows the ranking is highly sensitive to a single weight and that
   "the right answer" depends on what the scorer is told to value.
3. **Unit tests.** `tests/test_recommender.py` checks that the class-
   based API returns the expected top song for a pop/happy profile and
   that explanations are non-empty strings. Both tests pass.

I did not compute a numeric metric (precision / recall) because there is
no ground-truth "correct" ranking for subjective music preference.

---

## 8. Future Work

- **Diversity penalty.** Discount a song's score if a previous
  recommendation in the top-k is already by the same artist or in the
  same genre.
- **Multi-weight profiles.** Let the user set how much they care about
  genre versus mood versus energy, instead of fixing the weights.
- **Soft genre matching.** Treat "indie pop" and "indie" as partial
  matches, or build a small genre-similarity table.
- **Confidence threshold.** Refuse to return recommendations whose top
  score is below some floor, similar to the refusal guardrail in the
  Module 4 DocuBot tinker.
- **More songs, more moods.** Grow the catalog to at least 100 tracks
  so every genre/mood combination has real candidates.
- **Explainable negative reasons.** Show *why* a song didn't make the
  cut, not just why the chosen songs did.

---

## 9. Personal Reflection

What surprised me most was how little code it took to build something
that *feels* like a recommendation system. Twenty songs, four weights,
one sort - and the output looks real. That made me take the bias
discussion more seriously, not less. If this much effect comes from
this little code, then the people who pick the weights and the catalog
effectively pick the taste of the system's output.

Building the adversarial profile was the most valuable part. Watching
the scorer confidently hand back a slow Bon Iver song for a
"high-energy" request made the abstract idea of "model failure" very
concrete. The model isn't broken - it's doing exactly what I told it to
do. It just can't represent the real thing the user was asking for.
That gap between "scoring rule" and "what the user meant" is where
human judgment still belongs, even when a system looks smart.
