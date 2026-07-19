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


- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song:
  - Each song gets a single score from a weighted sum of two signals, with mood weighted more heavily so it drives the result:
  ``` 
  score = 
  W_mood * mood_match -> 1 if song.mood == favorite_mood, else 0 
  W_energy * energy_closeness -> # 1 - |song.energy - target_energy|
  ```
- How do you choose which songs to recommend:
  - By score every song in the catalog, then rank them from highest to lowest score and return the top n-songs



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



