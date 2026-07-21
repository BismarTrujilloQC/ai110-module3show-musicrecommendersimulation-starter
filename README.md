# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**My version** is a content-based recommender called *MoodFinder*. It represents each song as a row of attributes (genre, mood, energy, acousticness, and more) and each listener as a taste profile (`favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`). It scores every song against the profile with a weighted sum, ranks them, and returns the top _k_ with a plain-English reason for each pick. I also run six listener profiles — three ordinary and three adversarial — to see where the scoring logic breaks down.

---

## How The System Works

There are two strategies for building a recommender system:
1. **Content-based filtering**: *Intuition:* "here are songs whose attributes resemble what you already like". Builds profile from the feature of your favorites and matches new songs to it.
2. **Collaborative filtering**: *Intuition:* "people who behave like you also liked X". *Collaborative filtering knows nothing about the music*. Only sees *interaction matrix* -> who played, skipped or repeated what
  
**My version:** Will prioritize content-based filtering, using *energy* and *mood* to match user preferences. 


**`UserProfile` stores:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`.

**Scoring:** each song gets one score from a weighted sum, ordered by priority `mood > energy > genre > acoustic`:

```
score = 2.0 * mood_match        # 1 if song.mood == favorite_mood else 0
      + 1.5 * energy_closeness  # 1 - |song.energy - target_energy|
      + 1.0 * genre_match       # 1 if song.genre == favorite_genre else 0
      + 0.5 * acoustic_fit      # song.acousticness if likes_acoustic else 1 - song.acousticness
```

All four terms are on a 0→1 scale before weighting, so the weight alone sets importance. Max score = 5.0.

**Choosing recommendations:** score every song, rank highest to lowest, return the top _k_.

**Biases:**  This system is really biased toward the user's favorite mood and energy level. It will not recommend songs that are outside of those preferences, even if they are good recommendations.

---

## Sample Recommendation Output

```
 ============================================================
  TOP RECOMMENDATIONS                                       
============================================================

  1. Sunrise City  -  Neon Echo
     Score: 4.47 / 5.00
     Why we picked it:
       * matches your favorite mood (happy)
       * energy 0.82 is close to your target 0.80
       * matches your favorite genre (pop)

  2. Rooftop Lights  -  Indigo Parade
     Score: 3.44 / 5.00
     Why we picked it:
       * matches your favorite mood (happy)
       * energy 0.76 is close to your target 0.80

  3. Gym Hero  -  Max Pulse
     Score: 2.30 / 5.00
     Why we picked it:
       * energy 0.93 is close to your target 0.80
       * matches your favorite genre (pop)

  4. Concrete Kingdom  -  Kairo Blaze
     Score: 1.50 / 5.00
     Why we picked it:
       * energy 0.80 is close to your target 0.80

  5. Fiesta del Sol  -  Los Corazones
     Score: 1.44 / 5.00
     Why we picked it:
       * energy 0.84 is close to your target 0.80

============================================================
```
---
## Adversal profiles example
 ```
 ===========================================================
  [ADVERSARIAL] CONFLICTING ENERGY VS MOOD                  
============================================================

  1. Moonlit Adagio  -  Vienna Strings
     Score: 3.46 / 5.00
     Why we picked it:
       * matches your favorite mood (melancholic)
       * energy 0.24 is close to your target 0.95
       * matches your favorite genre (classical)
       * fits your non-acoustic preference

  2. Neon Pulse Drop  -  Volt Kandy
     Score: 1.97 / 5.00
     Why we picked it:
       * energy 0.95 is close to your target 0.95
       * fits your non-acoustic preference

  3. Iron Verdict  -  Ashfall
     Score: 1.95 / 5.00
     Why we picked it:
       * energy 0.97 is close to your target 0.95
       * fits your non-acoustic preference

  4. Gym Hero  -  Max Pulse
     Score: 1.95 / 5.00
     Why we picked it:
       * energy 0.93 is close to your target 0.95
       * fits your non-acoustic preference

  5. Storm Runner  -  Voltline
     Score: 1.89 / 5.00
     Why we picked it:
       * energy 0.91 is close to your target 0.95
       * fits your non-acoustic preference

============================================================


============================================================
  [ADVERSARIAL] ACOUSTIC LOVER, HIGH ENERGY                 
============================================================

  1. Neon Pulse Drop  -  Volt Kandy
     Score: 4.53 / 5.00
     Why we picked it:
       * matches your favorite mood (euphoric)
       * energy 0.95 is close to your target 0.95
       * matches your favorite genre (edm)
       * fits your acoustic preference

  2. Gym Hero  -  Max Pulse
     Score: 1.50 / 5.00
     Why we picked it:
       * energy 0.93 is close to your target 0.95
       * fits your acoustic preference

  3. Storm Runner  -  Voltline
     Score: 1.49 / 5.00
     Why we picked it:
       * energy 0.91 is close to your target 0.95
       * fits your acoustic preference

  4. Iron Verdict  -  Ashfall
     Score: 1.49 / 5.00
     Why we picked it:
       * energy 0.97 is close to your target 0.95
       * fits your acoustic preference

  5. Fiesta del Sol  -  Los Corazones
     Score: 1.48 / 5.00
     Why we picked it:
       * energy 0.84 is close to your target 0.95
       * fits your acoustic preference

============================================================


============================================================
  [ADVERSARIAL] GHOST PREFERENCES                           
============================================================

  1. Velvet Hours  -  Nyra Soul
     Score: 1.76 / 5.00
     Why we picked it:
       * energy 0.50 is close to your target 0.50
       * fits your non-acoustic preference

  2. Island Time  -  Sunny Roots
     Score: 1.70 / 5.00
     Why we picked it:
       * energy 0.55 is close to your target 0.50
       * fits your non-acoustic preference

  3. Midnight Coding  -  LoRoom
     Score: 1.52 / 5.00
     Why we picked it:
       * energy 0.42 is close to your target 0.50
       * fits your non-acoustic preference

  4. Dust & Diesel  -  Clay Hollow
     Score: 1.52 / 5.00
     Why we picked it:
       * energy 0.58 is close to your target 0.50
       * fits your non-acoustic preference

  5. Night Drive Loop  -  Neon Echo
     Score: 1.52 / 5.00
     Why we picked it:
       * energy 0.75 is close to your target 0.50
       * fits your non-acoustic preference

============================================================
 ```


---
## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

## Experiments You Tried

- **Reordering the weight priority** (`mood > energy > genre > acoustic`) is what
  makes a low-energy classical track beat the high-energy songs the "Conflicting
  Energy vs Mood" user asked for — mood's weight of 2.0 simply outvotes everything.
- **Running many different profiles** showed the catalog has almost no
  moderate-energy songs, so the "Ghost Preferences" user (target 0.50) gets weak,
  near-tied recommendations.

### Adversarial / Edge-Case Profiles

I designed three adversarial profiles to try to "trick" the scoring logic and
observed the top 5 recommendations each produced. The full terminal output for
each run is shown in the "Adversarial profiles example" section above.

**A. Conflicting energy vs. mood** — `energy 0.95` + `mood: melancholic`. A
near-silent classical track wins on mood alone despite the user asking for high
energy; the reason line still claims `energy 0.24 is close to your target 0.95`.

**B. Acoustic lover, high energy** — the catalog's acoustic songs are all
low-energy, so "acoustic + high energy" can't co-exist. The winner is labeled as
fitting the acoustic preference while actually being one of the least acoustic
tracks, because energy dominates the tie-break.

**C. Ghost preferences** — a genre and mood that don't exist in the catalog.
Those two terms silently score 0, so ranking quietly collapses to energy and
acoustic fit only, with no warning to the user.





## Limitations and Risks

- It only works on a tiny 20-song catalog, so recommendations run out fast.
- Genre and mood are exact-string matches — "chill" and "relaxed" never count as
  similar, and a genre that isn't in the catalog silently scores 0.
- With mood weighted highest, the system over-favors mood and can hand back a
  song whose energy is the opposite of what the user asked for.
- It does not understand lyrics, language, or artist, only the numeric/label
  features in the CSV.

I go deeper on these in the model card.

---

## Reflection

Building this made concrete that a recommender is only as good as the features and
weights it's given: the "prediction" is really just arithmetic over labels, and the
ranking reflects whatever the weights say matters most. The most striking moment was
watching a workout track win for a happy-pop listener purely because their energy dial
pointed at gym music — the system had no idea the mood was wrong.

That's also where bias and unfairness sneak in. Because genre and mood are exact
matches, listeners whose taste doesn't use the catalog's exact vocabulary get worse
results, and any genre under-represented in the data is effectively invisible. A real
recommender would amplify these gaps at scale, which is why knowing when to return
"no strong match" is as important as picking a winner.

See the full [**Model Card**](model_card.md) for intended use, limitations, and evaluation.



