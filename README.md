# CineMatch

A content-based movie recommendation web application that discovers films with similar stories, genres, casts, directors, and keywords.

Enter a movie title and CineMatch returns the five closest matches from the TMDB 5000 Movie Dataset.

## Features

- Cinematic, responsive Flask interface
- Movie title autocomplete
- Top-five content-based recommendations with match scores
- Movie release year, TMDB rating, and genres
- Optional TMDB poster integration
- Loading and invalid-title states

## How it works

The recommendation engine combines each film's overview, genres, keywords, top three cast members, and director into a single set of tags.

1. `CountVectorizer` converts those tags into numerical feature vectors.
2. Cosine similarity measures how closely each movie relates to the selected title.
3. The five highest-scoring movies are returned as recommendations.

## Tech stack

- Python
- Flask
- Pandas
- Scikit-learn
- NLTK
- HTML, CSS, and JavaScript
- TMDB API (optional poster images)

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in a browser. The first startup may take a few seconds while the model prepares the movie feature vectors.

## Poster images

The app works without a TMDB key and displays poster placeholders. To enable TMDB posters, I have set a TMDB v3 API key before starting the application:

```powershell
$env:TMDB_API_KEY="your_tmdb_v3_api_key"
python app.py
```
## Project structure

```text
app.py                  Flask routes and API endpoints
model.py                Content-based recommendation engine
templates/index.html    Application page
static/                 Styling and browser-side behaviour
tmdb_5000_movies.csv    Movie metadata dataset
tmdb_5000_credits.csv   Cast and crew dataset
```

## Dataset

This project uses the TMDB 5000 Movie Dataset. TMDB API data is used only for poster images when an API key is configured.
