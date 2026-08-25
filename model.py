"""The original notebook's content-based recommendation pipeline."""
import ast
from pathlib import Path

import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent


def convert(obj):
    return [item["name"] for item in ast.literal_eval(obj)]


def convert_cast(obj):
    return [item["name"] for item in ast.literal_eval(obj)[:3]]


def fetch_director(text):
    return [item["name"] for item in ast.literal_eval(text) if item["job"] == "Director"]


def stem(text):
    porter = PorterStemmer()
    return " ".join(porter.stem(word) for word in text.split())


class MovieRecommender:
    def __init__(self):
        movies = pd.read_csv(BASE_DIR / "tmdb_5000_movies.csv")
        credits = pd.read_csv(BASE_DIR / "tmdb_5000_credits.csv")
        movies = movies.merge(credits, on="title")
        display = movies[["movie_id", "title", "overview", "genres", "release_date", "vote_average"]].copy()

        # The following transformations mirror movie_recommender_system.ipynb.
        movies = movies[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]
        movies.dropna(inplace=True)
        movies["genres"] = movies["genres"].apply(convert)
        movies["keywords"] = movies["keywords"].apply(convert)
        movies["cast"] = movies["cast"].apply(convert_cast)
        movies["crew"] = movies["crew"].apply(fetch_director)
        movies["overview"] = movies["overview"].apply(lambda value: value.split())
        for column in ["genres", "keywords", "cast", "crew"]:
            movies[column] = movies[column].apply(lambda values: [value.replace(" ", "") for value in values])
        movies["tags"] = movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]
        self.movies = movies[["movie_id", "title", "tags"]].copy()
        self.movies["tags"] = self.movies["tags"].apply(lambda values: " ".join(values)).str.lower().apply(stem)
        vectorizer = CountVectorizer(max_features=5000, stop_words="english")
        vectors = vectorizer.fit_transform(self.movies["tags"]).toarray()
        self.similarity = cosine_similarity(vectors)

        display["genres"] = display["genres"].apply(convert)
        display["year"] = display["release_date"].fillna("").str[:4]
        self.details = display.drop_duplicates("movie_id").set_index("movie_id").to_dict("index")
        self.titles = self.movies["title"].drop_duplicates().tolist()
        self.title_lookup = {title.casefold(): title for title in self.titles}

    def suggestions(self, query, limit=8):
        query = query.strip().casefold()
        if not query:
            return []
        first = [title for title in self.titles if title.casefold().startswith(query)]
        rest = [title for title in self.titles if query in title.casefold() and title not in first]
        return (first + rest)[:limit]

    def recommend(self, title):
        title = self.title_lookup.get(title.strip().casefold())
        if not title:
            return None
        movie_index = self.movies[self.movies["title"] == title].index[0]
        # Same top-five sorted cosine-similarity ranking as the notebook.
        movie_list = sorted(enumerate(self.similarity[movie_index]), reverse=True, key=lambda item: item[1])[1:6]
        recommendations = []
        for index, score in movie_list:
            movie = self.movies.iloc[index]
            detail = self.details.get(movie.movie_id, {})
            recommendations.append({"id": int(movie.movie_id), "title": movie.title, "score": round(float(score) * 100, 1), "year": detail.get("year") or "—", "rating": detail.get("vote_average"), "genres": detail.get("genres", [])[:3]})
        return {"title": title, "recommendations": recommendations}
