import pandas as pd
import duckdb as db

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

df_salade = pd.read_csv("df_salade.csv")

# Crée et entraîne le vectoriseur
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(df_salade["combined_features"])

nn_model = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=30)
nn_model.fit(X_tfidf)  # là le modèle est entraîné

_, indices = nn_model.kneighbors(X_tfidf)

import joblib

joblib.dump(indices, "recos.pkl")
