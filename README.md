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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



