"""
Funciones de extracción de datos desde la Spotify API.
Diseñado para construir el dataset propio del proyecto.
"""

import time
import pandas as pd
from tqdm import tqdm
from .spotify_client import get_client


def get_audio_features(track_ids: list, sp=None) -> pd.DataFrame:
    """
    Obtiene las audio features de una lista de track IDs.
    Spotify permite hasta 100 tracks por llamada.

    Args:
        track_ids: Lista de Spotify track IDs
        sp: Cliente Spotipy (se crea uno nuevo si no se pasa)

    Returns:
        DataFrame con audio features por canción
    """
    if sp is None:
        sp = get_client()

    all_features = []
    for i in tqdm(range(0, len(track_ids), 100), desc="Extrayendo audio features"):
        batch = track_ids[i:i + 100]
        features = sp.audio_features(batch)
        all_features.extend([f for f in features if f is not None])
        time.sleep(0.1)

    return pd.DataFrame(all_features)


def get_tracks_from_playlist(playlist_id: str, sp=None) -> pd.DataFrame:
    """
    Extrae todas las canciones de una playlist con sus metadatos.

    Args:
        playlist_id: ID de la playlist de Spotify
        sp: Cliente Spotipy

    Returns:
        DataFrame con tracks (id, nombre, artista, álbum, popularidad, fecha)
    """
    if sp is None:
        sp = get_client()

    tracks = []
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results["items"]:
            track = item.get("track")
            if track is None:
                continue
            tracks.append({
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "artist_id": track["artists"][0]["id"],
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "popularity": track["popularity"],
                "duration_ms": track["duration_ms"],
                "explicit": track["explicit"],
            })
        results = sp.next(results) if results["next"] else None

    return pd.DataFrame(tracks)


def get_genre_playlists(genres: list, limit_per_genre: int = 5, sp=None) -> dict:
    """
    Busca playlists representativas para una lista de géneros.

    Args:
        genres: Lista de géneros ('pop', 'rock', 'jazz', etc.)
        limit_per_genre: Número de playlists por género
        sp: Cliente Spotipy

    Returns:
        Dict {genre: [playlist_ids]}
    """
    if sp is None:
        sp = get_client()

    genre_playlists = {}
    for genre in tqdm(genres, desc="Buscando playlists por género"):
        results = sp.search(q=f"genre:{genre}", type="playlist", limit=limit_per_genre)
        playlists = results["playlists"]["items"]
        genre_playlists[genre] = [p["id"] for p in playlists if p]
        time.sleep(0.2)

    return genre_playlists
