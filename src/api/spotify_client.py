"""
Cliente para la Spotify Web API usando Spotipy.
Gestiona autenticación y proporciona métodos de extracción de datos.
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


def get_client(auth_flow: str = "client_credentials") -> spotipy.Spotify:
    """
    Devuelve un cliente autenticado de Spotipy.

    Args:
        auth_flow: 'client_credentials' para datos públicos (sin usuario),
                   'oauth' para acceder a datos de usuario (historial, playlists).

    Returns:
        Instancia autenticada de spotipy.Spotify
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise EnvironmentError(
            "Faltan credenciales. Copia .env.example a .env y rellena "
            "SPOTIFY_CLIENT_ID y SPOTIFY_CLIENT_SECRET."
        )

    if auth_flow == "client_credentials":
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    elif auth_flow == "oauth":
        scopes = "user-library-read user-top-read playlist-read-private"
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback"),
            scope=scopes
        )
    else:
        raise ValueError(f"auth_flow desconocido: {auth_flow}")

    return spotipy.Spotify(auth_manager=auth_manager)
