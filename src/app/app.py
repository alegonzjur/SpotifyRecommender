"""
SpotifyMusicRecommender — API Flask
Expone el modelo recomendador content-based como servicio web.
"""

import os
import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)

# ── Rutas de datos ────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "..", "..", "data", "processed", "tracks_powerbi.csv")
MODEL_PATH = os.path.join(BASE_DIR, "..", "..", "models", "scaler.pkl")

# ── Carga de datos al arrancar ────────────────────────────────────────────────
print("Cargando dataset...")
df = pd.read_csv(DATA_PATH)

print("Cargando scaler...")
with open(MODEL_PATH, "rb") as f:
    scaler = pickle.load(f)

FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo"
]

X_scaled = scaler.transform(df[FEATURES])
print(f"Dataset listo: {len(df):,} canciones ✅")


# ── Función recomendadora ─────────────────────────────────────────────────────
def recomendar(titulo, artista=None, n=10):
    mask = df["track_name"].str.contains(titulo, case=False, na=False)
    if artista:
        mask &= df["artists"].str.contains(artista, case=False, na=False)

    candidatos = df[mask]
    if candidatos.empty:
        return None, f"No se encontró ninguna canción con el título '{titulo}'"

    idx = candidatos["popularity"].idxmax()
    ref = df.loc[idx]

    filtro = pd.Series([True] * len(df), index=df.index)
    filtro &= df["track_genre"] == ref["track_genre"]
    filtro &= df["cluster"]     == ref["cluster"]
    filtro.iloc[idx] = False

    indices_filtrados = df[filtro].index.tolist()
    if not indices_filtrados:
        return None, "No hay canciones suficientes con ese filtro."

    vector_ref  = X_scaled[idx].reshape(1, -1)
    similitudes = cosine_similarity(vector_ref, X_scaled[indices_filtrados])[0]

    sim_norm = (similitudes - similitudes.min()) / (similitudes.max() - similitudes.min() + 1e-9)
    pop_vals = df.loc[indices_filtrados, "popularity"].values
    pop_norm = (pop_vals - pop_vals.min()) / (pop_vals.max() - pop_vals.min() + 1e-9)
    score    = 0.7 * sim_norm + 0.3 * pop_norm

    top_locales  = np.argsort(score)[::-1][: n * 5]
    top_globales = [indices_filtrados[i] for i in top_locales]

    resultado = df.iloc[top_globales][
        ["track_name", "artists", "track_genre", "cluster_nombre", "popularity", "valence", "energy", "danceability"]
    ].copy()
    resultado["similitud"] = similitudes[top_locales].round(4)
    resultado["score"]     = score[top_locales].round(4)
    resultado = (resultado
                 .drop_duplicates(subset="track_name", keep="first")
                 .head(n)
                 .reset_index(drop=True))
    resultado.index += 1

    referencia = {
        "track_name":    ref["track_name"],
        "artists":       ref["artists"],
        "track_genre":   ref["track_genre"],
        "cluster_nombre": ref["cluster_nombre"],
        "popularity":    int(ref["popularity"]),
    }

    recomendaciones = resultado[["track_name", "artists", "track_genre",
                                  "popularity", "similitud"]].to_dict(orient="records")

    return {"referencia": referencia, "recomendaciones": recomendaciones}, None


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "canciones": len(df)})

@app.route("/recomendar")
def recomendar_endpoint():
    titulo  = request.args.get("titulo", "").strip()
    artista = request.args.get("artista", "").strip() or None
    n       = min(int(request.args.get("n", 10)), 20)

    if not titulo:
        return jsonify({"error": "El parámetro 'titulo' es obligatorio"}), 400

    resultado, error = recomendar(titulo, artista, n)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True, port=5000)