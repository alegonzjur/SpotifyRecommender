# Guía de la Spotify Web API

## Endpoints principales

### Audio Features
`GET https://api.spotify.com/v1/audio-features/{id}`

| Feature | Rango | Descripción |
|---------|-------|-------------|
| danceability | 0.0–1.0 | Adecuación para bailar |
| energy | 0.0–1.0 | Intensidad y actividad percibida |
| valence | 0.0–1.0 | Positividad musical |
| tempo | BPM | Tempo estimado |
| acousticness | 0.0–1.0 | Probabilidad de ser acústica |
| instrumentalness | 0.0–1.0 | Probabilidad de no contener voz |
| speechiness | 0.0–1.0 | Presencia de palabras habladas |
| liveness | 0.0–1.0 | Probabilidad de grabación en directo |
| loudness | dB | Volumen medio (normalmente entre -60 y 0 dB) |

## Flujos de autenticación

### Client Credentials (datos públicos)
Válido para: audio features, metadatos de tracks, búsquedas, playlists públicas.
No requiere login de usuario. Ideal para construir el dataset.

### OAuth 2.0 (datos de usuario)
Válido para: historial de escuchas, playlists privadas, canciones guardadas.
Necesario para la fase de collaborative filtering.

## Rate Limits
- ~100 req/s con client_credentials en condiciones normales
- Añadir `time.sleep(0.1)` entre lotes grandes como precaución
