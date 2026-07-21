# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodFinder** 

---

## 2. Intended Use  

recommender suggests songs from a short list and matches listener's stated taste. It assumes the user can describe their taste as a favorite genre, a favorite mood, a target energy level, and if they like acoustic music.

---

## 3. How the Model Works  

Each song has a genre, a mood, and an energy level, and is marked as more or less acoustic. The model compares those to what the listener asked for and gives points for each match: the most points for mood, then energy, then genre, and the fewest for the acoustic fit. It adds the points into one score, then ranks the songs and returns the highest scorers.

---

## 4. Data  

The initial list has 20 songs spread across about many genres and a wide range of moods. Each song also lists numeric features like energy, tempo, valence, danceability, and acousticness.

---

## 5. Strengths  

The system works well when a listener's preferences agree with each other, like a Chill Lofi fan who wants low energy and acoustic music.

---

## 6. Limitations and Bias 

System quietly ignores listeners who want moderate energy music. Most of the songs in the catalog are either  calm or  energetic, with very little in the middle.

---

## 7. Evaluation  


**Profiles tested:** three normal listeners:
- **High-Energy Pop** (pop, happy, high energy), 
- **Chill Lofi** (lofi, chill, low energy, acoustic),
- **Deep Intense Rock** (rock, intense, high energy)

- plus three edge-case profiles to trip the scorer: 
    - **Conflicting Energy** (high energy but a sad mood), 
    - **Acoustic Lover** (acoustic but high energy),
    - **Ghost Preferences** (a genre and mood that don't exist in the catalog).

**What surprised me:** Workout song "Gym Hero" kept showing up for the High-Energy Pop fan, even though it's tagged as intense, not happy. 

**The reason** Is that this listener set their energy dial almost to the top (0.90), and the loudest songs at that level are gym anthems. The system gives "Gym Hero" credit for being pop *and* high energy, and those two points outweigh its wrong mood.

---

## 8. Future Work  

I would add more songs to fill the gaps, especially moderate energy songs. I would also let similar moods like chill and relaxed count as partial matches instead of all or nothing.

---

## 9. Personal Reflection  

- Building this taught me that a recommender is only as smart as the numbers and labels it's given.
- The most interesting moment was seeing a workout song win for a high-energy pop listener simply because their energy setting pointed at gym music
- It made me realize that real music apps must handle messy, conflicting taste and that a good recommendation is often as much about knowing when to say no strong match as it is about picking a winner.
