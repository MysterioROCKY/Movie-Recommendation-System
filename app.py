import os
from functools import lru_cache

import requests
from flask import Flask, jsonify, render_template, request
from model import MovieRecommender

app = Flask(__name__)
recommender = MovieRecommender()


@lru_cache(maxsize=512)
def poster_for(movie_id):
    """Posters are optional; API keys stay only on the server."""
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        return None
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}", params={"api_key": api_key}, timeout=4)
        response.raise_for_status()
        path = response.json().get("poster_path")
        return f"https://image.tmdb.org/t/p/w500{path}" if path else None
    except requests.RequestException:
        return None


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/suggestions")
def suggestions():
    return jsonify({"suggestions": recommender.suggestions(request.args.get("q", ""))})


@app.post("/api/recommendations")
def recommendations():
    title = (request.get_json(silent=True) or {}).get("title", "")
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Enter a movie title to get recommendations."}), 400
    result = recommender.recommend(title)
    if not result:
        return jsonify({"error": f'“{title.strip()}” is not in this movie catalog.'}), 404
    for movie in result["recommendations"]:
        movie["poster"] = poster_for(movie["id"])
        movie["rating"] = round(float(movie["rating"]), 1) if movie["rating"] is not None else None
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
