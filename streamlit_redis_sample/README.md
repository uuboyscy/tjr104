# Taiwan Population Map (Streamlit + Redis)

A dynamic population density map of Taiwan using Streamlit, Redis, and PyDeck.
Data granularity adjusts based on zoom using Geohash precision.

## Quick Start

### 1. Start Redis
```bash
docker compose up -d
```
*Access Redis Insight at [http://localhost:8001](http://localhost:8001)*

### 2. Install Dependencies
```bash
uv sync
```

### 3. Generate Data
Generates 100k synthetic points and aggregates them in Redis.
```bash
uv run python generator.py
```

### 4. Run App
```bash
uv run streamlit run app.py
```
*Open [http://localhost:8501](http://localhost:8501)*
