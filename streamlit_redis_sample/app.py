import streamlit as st
import redis
import pandas as pd
import pydeck as pdk
import geohash
import numpy as np

# Page Config
st.set_page_config(layout="wide", page_title="Taiwan Population Map")

# Redis Connection
@st.cache_resource
def get_redis_client():
    return redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    redis_client = get_redis_client()
    redis_client.ping()
except Exception as e:
    st.error(f"Could not connect to Redis: {e}")
    st.stop()

st.title("Taiwan Population Density Visualization")
st.markdown("Dynamic aggregation based on zoom level. Data stored in **Redis** independently for each precision.")

# Sidebar Controls
st.sidebar.header("Controls")

# Map Zoom / Resolution
# We use this slider to determine both the initial map zoom and the data granularity
zoom_level = st.sidebar.slider(
    "Map Zoom Level", 
    min_value=4.0, 
    max_value=12.0, 
    value=6.0, 
    step=0.5,
    help="Zooming in increases data granularity (higher precision Geohashes)."
)

# Determine Precision Logic
# Precision 4: ~20km error (Good for Zoom 4-6)
# Precision 5: ~2.4km error (Good for Zoom 6-9)
# Precision 6: ~0.6km error (Good for Zoom 9-11)
# Precision 7: ~0.07km error (Good for Zoom 11+)
if zoom_level < 6.0:
    precision = 4
    radius = 18000
    elevation_scalar = 50
elif zoom_level < 8.5:
    precision = 5
    radius = 2200
    elevation_scalar = 100
elif zoom_level < 10.5:
    precision = 6
    radius = 500
    elevation_scalar = 300
else:
    precision = 7
    radius = 70
    elevation_scalar = 1000

st.sidebar.info(f"**Current Precision:** Geohash-{precision}")

# Load Data
@st.cache_data(ttl=60)
def load_data(prec):
    key = f"population:{prec}"
    try:
        data = redis_client.hgetall(key)
    except Exception as e:
        st.error(f"Redis Error: {e}")
        return pd.DataFrame()
        
    if not data:
        return pd.DataFrame()

    rows = []
    for gh, count in data.items():
        try:
            # decode returns (lat, lon)
            lat, lon = geohash.decode(gh)
            count = int(count)
            rows.append({"geohash": gh, "lat": lat, "lon": lon, "count": count})
        except Exception:
            continue
            
    return pd.DataFrame(rows)

with st.spinner(f"Loading data for Geohash-{precision}..."):
    df = load_data(precision)

if df.empty:
    st.warning("No data found for this precision level. Ensure `generator.py` has been run.")
else:
    st.sidebar.metric("Visible Clusters", len(df))
    st.sidebar.metric("Total Population (Sampled)", df['count'].sum())

    # PyDeck Layer
    layer = pdk.Layer(
        "ColumnLayer",
        data=df,
        get_position=["lon", "lat"],
        get_elevation="count",
        elevation_scale=elevation_scalar,
        radius=radius,
        get_fill_color=[255, 165, 0, 140],
        pickable=True,
        auto_highlight=True,
    )

    # Tooltip
    tooltip = {
        "html": "<b>Geohash:</b> {geohash}<br/><b>Count:</b> {count}<br/><b>Precision:</b> " + str(precision),
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    # View State
    view_state = pdk.ViewState(
        latitude=23.6,
        longitude=121.0,
        zoom=zoom_level,
        pitch=45,
        bearing=0
    )

    # Render
    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip
        )
    )

st.markdown("---")
st.caption("Generated with Streamlit, Redis, and PyDeck.")
