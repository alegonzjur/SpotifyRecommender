# 🎵 Spotify Music Recommender

Sistema de análisis y recomendación musical construido sobre la API oficial de Spotify. Actualmente, Spotify ha eliminado el acceso a las características de audio desde su API, por tanto, se utilizará un dataset recolectado previamente a la creación de las restricciones de la API.

## Objetivos del proyecto

- Realizar análisis exploratorio de características de audio
- Segmentar canciones mediante técnicas de clustering
- Desarrollar un sistema recomendador híbrido (content-based + collaborative filtering)
- Visualizar insights en Power BI y exponer recomendaciones vía API REST

## Estructura del proyecto

```
spotify-recommender/
├── data/
│   ├── raw/                # Datos originales extraídos de la API (no editar)
│   ├── processed/          # Datos limpios y transformados
│   └── external/           # Datasets de terceros (Last.fm, Kaggle)
├── notebooks/
│   ├── 01_eda_audio_features.ipynb
│   ├── 02_clustering.ipynb
│   └── 03_recommender_model.ipynb
├── src/
│   ├── data/               # Limpieza, transformación y carga
│   ├── models/             # Modelos de recomendación
│   └── visualization/      # Helpers de visualización
├── dashboard/              # Archivo .pbix y documentación del dashboard Power BI
├── reports/
│   └── figures/            # Gráficos exportados para documentación
├── tests/                  # Tests unitarios
├── docs/                   # Documentación técnica adicional
├── .env.example            # Variables de entorno necesarias
├── requirements.txt
└── README.md
```

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/spotify-recommender.git
cd spotify-recommender

# 2. Crear entorno virtual (Anaconda recomendado)
conda create -n spotify-recommender python=3.11
conda activate spotify-recommender

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales
cp .env.example .env
# Editar .env con tus credenciales de Spotify Developer
```

## Fases del proyecto

| Fase | Descripción | Estado |
|------|-------------|--------|
| 1 | EDA y caracterización | 🔄 En progreso |
| 2 | Clustering de canciones | ⏳ Pendiente |
| 3 | Modelo recomendador | ⏳ Pendiente |
| 4 | Dashboard Power BI | ⏳ Pendiente |
| 5 | API REST de recomendaciones | ⏳ Pendiente |

## Stack tecnológico

- **Análisis**: pandas, numpy, scikit-learn
- **Visualización**: matplotlib, seaborn, plotly
- **Dashboard**: Power BI Desktop
- **API**: Flask / FastAPI
- **Automatización futura**: n8n
