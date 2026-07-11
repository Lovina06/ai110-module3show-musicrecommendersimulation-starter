# 🎧 Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0**

A simple song recommender. It picks songs based on what you say you like.

---

## 2. Goal / Task

VibeFinder suggests a top-5 list of songs for one user.

It looks at four things a user tells it:

- favorite genre
- favorite mood
- how much energy they want
- whether they like acoustic songs

It does not learn over time. It just scores every song once, based on these four inputs, and returns the best matches.

---

## 3. Data Used

The dataset is `data/songs.csv`. It has **10 songs**.

Each song has:

- title and artist
- genre (pop, lofi, rock, ambient, jazz, synthwave, indie pop)
- mood (happy, chill, intense, relaxed, focused, moody)
- energy, tempo, valence, danceability, and acousticness (all numbers)

**Limits:**

- Only 10 songs total, so results repeat a lot.
- No classical, EDM, hip-hop, metal, or world music.
- No "angry" or "nostalgic" mood, and others are missing too.
- Some genres only have one song (like rock and jazz), so those users get almost no real choice.

---

## 4. Algorithm Summary (Plain Language)

Every song gets a score. Higher score = better match. Here's how the score is built:

- **Genre match:** If the song's genre matches what the user picked, add points.
- **Mood match:** If the song's mood matches what the user picked, add points.
- **Energy closeness:** The closer the song's energy is to what the user wants, the more points it gets. If it's way off, it gets few or no points.
- **Acoustic bonus:** If the user says they like acoustic music, and the song is acoustic enough, add a bonus point.

All the points are added up. Songs are sorted highest score first. The top 5 are shown to the user, along with a short explanation of why each one scored the way it did.

There is no penalty for a bad match. A wrong genre or mood just adds zero points — it never subtracts.

---

## 5. Observed Behavior / Biases

**Energy and genre matter more than mood.** Mood is worth the least in the scoring, so a song can win even with the wrong mood, as long as the genre and energy are close enough.

**Example:** A user who wants "happy pop" music still sees `Gym Hero` near the top, even though its mood is `intense`, not `happy`. That's because `Gym Hero` is one of only two pop songs in the whole dataset, and its energy is close to what most users ask for. It keeps showing up not because it's happy — but because there's nothing else competing for the "pop" spot.

**Bigger picture:** because the catalog is so small, and mood barely affects the score, users can easily get songs that "sort of" fit but don't actually match how they say they feel.

---

## 6. Evaluation Process

We tested VibeFinder with 9 different user profiles, on purpose picking some that were tricky or contradictory:

- A "sad but high-energy pop" profile, to see if mismatched mood gets caught (it doesn't).
- Energy set to the lowest (0.0) and highest (1.0) possible, to check the edges.
- A genre that doesn't exist in the dataset ("polka"), to see if it breaks (it doesn't — it just quietly ignores genre).
- A missing mood (`None`) and a fully blank profile, to see how the system handles missing info.
- Energy set way outside the normal range (1.5), to see if bad input causes problems.
- A "loves acoustic but wants high energy" profile — a real-world contradiction — to see if the system notices (it doesn't).
- A "happy pop" profile at two different energy levels, added specifically to explain why `Gym Hero` keeps appearing (see Section 5).

We then compared pairs of these profiles side by side. For example:

- Flipping energy from low to high completely flipped the results — that makes sense, since energy is a sliding scale.
- Two very different moods (sad vs. intense), both paired with the same genre and energy, gave almost the same top results — showing that mood barely matters compared to genre and energy.

**What surprised us:** the system never crashes, even with missing or broken input. But that's because it quietly ignores bad data instead of flagging it. The biggest surprise was that a wrong mood costs a song nothing — it can still win.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**

- A classroom project to practice building and testing a recommender system.
- A way to learn how scoring, ranking, and explanations work together.
- A tool for exploring bias and edge cases in a simple rule-based system.

**Not intended for:**

- Real music recommendations for real users. The dataset is far too small and made-up.
- Any use involving real personal data or user profiles.
- Any claim that this system understands music taste well. It only checks a few surface-level features (genre, mood, energy, acoustic), not the full picture of what makes someone like a song.
- Production or commercial use of any kind.

---

## 8. Ideas for Improvement

1. **Add a penalty for mismatches**, not just zero points, so a wrong genre or mood actually lowers a song's score instead of just not helping it.
2. **Check for bad or contradictory input**, like energy above 1.0 or preferences that don't really go together (like "loves acoustic" + "wants max energy"), instead of silently ignoring the problem.
3. **Use a bigger, more varied dataset**, and use more of the data we already have (like tempo and valence), so recommendations feel more personal instead of falling back on energy alone.
