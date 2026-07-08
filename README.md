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

Noticed a small inconsistency worth fixing before this goes in your final doc: this section says mood is "excluded from scoring", but your finalized Algorithm Recipe includes a MOOD_MATCH_BONUS = 1.0. Here's the reconciled version:
How The System Works
Real-world recommendation systems like Spotify's or YouTube's rarely rely on a single method — they blend collaborative filtering (what similar users liked) with content-based filtering (what a piece of content is actually like) and layer in contextual signals such as time of day, recent skips, and session behavior, all computed through learned embeddings rather than hand-picked features. My version is a simplified, purely content-based recommender: it scores each song by how close its audio attributes are to a user's preferences, plus small bonuses for categorical matches, rather than just favoring the "highest" or "most popular" values. This distance-based scoring is combined with a ranking layer that goes beyond simple sorting — enforcing diversity (capping same-artist recommendations) and lightly rewarding genre/mood matches without making either a hard filter. My system prioritizes relevance to individual taste over popularity or novelty, and treats "vibe" as a combination of measurable audio traits — acknowledging that this hand-engineered approach captures a real but incomplete picture, since it can't sense qualities like instrumentation texture the way a learned embedding model eventually could.
What features does each Song use?
Song
├── id, title, artist (metadata — not used in scoring)
├── genre, mood (soft signals — small bonus points, not hard filters)
└── energy, valence, danceability, acousticness, tempo_bpm (numeric similarity features)

id, title, artist — identifiers, excluded from scoring
genre — categorical soft signal, contributes +2.0 bonus points on exact match
mood — categorical soft signal, contributes +1.0 bonus points on exact match
energy, valence, danceability, acousticness (0–1) — scored via distance-to-target similarity
tempo_bpm — scored the same way, but normalized to 0–1 first

(Note: mood is a categorical bonus here rather than excluded — while it's true mood correlates with energy+valence, keeping it as a small separate bonus lets exact mood labels serve as a light tie-breaker without duplicating the numeric scoring logic.)
Finalized Algorithm Recipe
pythonGENRE_MATCH_BONUS = 2.0
MOOD_MATCH_BONUS = 1.0

def similarity_points(song_value, target_value, max_points=2.0):
distance = abs(song_value - target_value)
return max_points \* (1 - distance)

final_score = (
(2.0 if song.genre == favorite_genre else 0) +
(1.0 if song.mood == favorite_mood else 0) +
similarity_points(song.energy, target_energy) +
similarity_points(song.valence, target_valence) +
similarity_points(song.danceability, target_danceability) +
similarity_points(song.acousticness, target_acousticness) +
similarity_points(song.tempo_normalized, target_tempo_normalized)
)
Max possible score: 13.0 (2 + 1 + 2×5). Ranking then sorts by final_score, excludes listening history, and caps results per artist.
Potential Biases

Genre over-weighting: at +2.0, a genre match equals a near-perfect single-feature numeric match — this system might over-prioritize genre, missing great songs that fit the user's mood/vibe but sit in a different genre.
Linear similarity may not match human perception: small feature differences and large ones are penalized proportionally, when humans may barely notice small gaps but strongly notice large ones — a curve-based (e.g., Gaussian) falloff would model this more naturally.
Mood/genre are subjective, human-assigned labels: two songs could feel identical in vibe but carry different mood/genre tags, and the system has no way to detect that mismatch.
No collaborative signal: purely content-based scoring can't capture "people with similar taste also liked this," so it will systematically favor numerically similar songs over songs that are simply well-loved by similar listeners.
Limited novelty/discovery: because scoring only rewards closeness to existing stated preferences, the system won't proactively surface things outside the user's known taste profile.

What information does UserProfile store?

preferred_energy, preferred_valence, preferred_danceability, preferred_acousticness, preferred_tempo — the user's target value for each feature (not "high/low," but a specific preferred point, per the distance-based scoring approach)
feature_weights — how much each feature matters to this user (defaults to the recipe's weights: valence 0.30, energy 0.30, acousticness 0.20, danceability 0.10, tempo 0.10)
listening_history — list of song IDs already heard, used to exclude repeats or apply novelty logic
preferred_genre (optional) — used only for the small genre-match bonus, never as a hard filter

UserProfile
├── preferred\_\* values (one per scored feature)
├── feature_weights (personalizes importance per user)
├── listening_history (avoid repeats)
└── preferred_genre (optional) (soft bonus only)
How does Recommender compute a score for each song?

For each feature, compute a distance-based score against the user's preferred value:

feature_score = exp(-(|song_value - user_preference|)^2 / (2 \* sigma^2))

Combine feature scores using the user's weights:

weighted_score = Σ (weight_i × feature_score_i)

Add a small genre bonus if applicable:

final_score = weighted_score + (0.05 if song.genre == user.preferred_genre else 0)
How do you choose which songs to recommend?
This is the Ranking Rule — a separate step from scoring:

Compute final_score for every candidate song
Sort descending by score
Filter out songs already in listening_history
Enforce diversity: cap recommendations per artist (e.g., max 1–2 per artist)
Return the top N songs after filtering

Song list → Score each song → Sort by score → Apply diversity/history filters → Top N results
This separation means scoring answers "how good is this song for this user" independently per song, while ranking answers "what's the best list to actually show," which needs the full candidate set and business rules layered on top.

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

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

### Sample Recommendation Output

Loaded 10 songs from data/songs.csv

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City — by Neon Echo
   Score: 4.96
   Why: genre match (+2.0), mood match (+1.0), energy closeness (+2.0)

---

2. Gym Hero — by Max Pulse
   Score: 3.74
   Why: genre match (+2.0), energy closeness (+1.7)

---

3. Rooftop Lights — by Indigo Parade
   Score: 2.92
   Why: mood match (+1.0), energy closeness (+1.9)

---

4. Night Drive Loop — by Neon Echo
   Score: 1.90
   Why: energy closeness (+1.9)

---

5. Storm Runner — by Voltline
   Score: 1.78
   Why: energy closeness (+1.8)

---
