# CineMatch — Movie Recommendation System

A polished Flask web app for this repository's content-based movie recommender. Search a title and receive its five closest matches from a catalogue of 4,800+ films.

The recommendation logic is preserved from `movie_recommender_system.ipynb`: overview, genres, keywords, top-three cast members and director form movie tags; `CountVectorizer(max_features=5000, stop_words="english")` creates vectors, and cosine similarity returns the top five results.

## Features

- Responsive dark cinema-themed design
- Movie-title autocomplete, loading and not-found states
- Real-time top-five recommendations and similarity scores
- Movie years, genres and ratings from the TMDB dataset
- Optional live TMDB posters, with the API key stored server-side

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. Initial startup builds the similarity matrix from the two CSV files, so it takes a few seconds.

To show live posters, create a free TMDB API key, set `TMDB_API_KEY` in your environment, and never commit that key. The app works without it using designed poster placeholders.

## Deploy on Render

1. Push these changes to GitHub.
2. In [Render](https://render.com), choose **New → Blueprint**, then select this repository. It will use `render.yaml`.
3. Optionally add the secret `TMDB_API_KEY` environment variable in Render.
4. Deploy. Use the resulting public URL as your resume’s **Live Demo** link.

For a manually-created service, use `pip install -r requirements.txt` as the build command and `gunicorn app:app` as the start command.

## Resume entry

**CineMatch — Content-Based Movie Recommendation System** | Python, Flask, Scikit-learn, Pandas, JavaScript

Built and deployed a responsive movie-discovery web app using NLP feature engineering and cosine similarity across 4,800+ TMDB titles; delivered real-time top-five recommendations with autocomplete and optional TMDB poster integration.

Include both **Live Demo** and **GitHub** links beside this project.
