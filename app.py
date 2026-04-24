import streamlit as st
import time
import random
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Crowd Intelligence NOC", layout="wide")

# 🔥 DARK UI
st.markdown("""
<style>
.stApp { background-color: #0E1117; }
html, body, [class*="css"] { color: white !important; }

[data-testid="stMetric"] {
    background-color: #1E222A;
    padding: 12px;
    border-radius: 12px;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: bold;
}

div.stButton > button {
    background-color: #2E86FF !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
}

/* 🔴 Blinking alert */
@keyframes blink {
    0% {opacity: 1;}
    50% {opacity: 0.4;}
    100% {opacity: 1;}
}

.blink-alert {
    animation: blink 1s infinite;
    background-color: #3a1a1a;
    border-left: 5px solid red;
    padding: 10px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

st.title("🖥️ Crowd Intelligence Command Center")

# LOCATIONS
LOCATIONS = {
    "Vashi Station": {"video": "videos/station.mp4", "lat": 19.0633, "lon": 73.0006},
    "Airoli Park": {"video": "videos/park.mp4", "lat": 19.1590, "lon": 72.9986},
    "Grand Central Mall": {"video": "videos/mall.mp4", "lat": 19.2183, "lon": 73.0865}
}

# Session state
if "run" not in st.session_state:
    st.session_state.run = False

if "counts" not in st.session_state:
    st.session_state.counts = {loc: 10 for loc in LOCATIONS}

if "history" not in st.session_state:
    st.session_state.history = {loc: [] for loc in LOCATIONS}

if "alert_spike" not in st.session_state:
    st.session_state.alert_spike = {loc: 0 for loc in LOCATIONS}

if "alert_trend" not in st.session_state:
    st.session_state.alert_trend = {loc: 0 for loc in LOCATIONS}

# Controls
c1, c2 = st.columns(2)
if c1.button("▶ START"):
    st.session_state.run = True
if c2.button("⏹ STOP"):
    st.session_state.run = False

kpi_placeholder = st.empty()

cols = st.columns(3)
tiles = [cols[0].empty(), cols[1].empty(), cols[2].empty()]

# Heatmap
st.markdown("---")
st.subheader("🗺️ Crowd Heatmap")
heatmap_placeholder = st.empty()

if st.session_state.run:

    while True:

        if not st.session_state.run:
            time.sleep(0.2)
            continue

        total = 0
        alerts = []
        heatmap_data = []

        for i, (loc, cfg) in enumerate(LOCATIONS.items()):

            # 🎯 Simulated AI
            ai = random.randint(5, 25)

            # 📶 Simulated telecom
            telco = ai + random.randint(-3, 5)

            # 🔀 Fusion
            final = int((ai + telco) / 2)
            total += final

            # 📈 History
            st.session_state.history[loc].append(final)

            # 🔮 Prediction
            pred = int(final + random.randint(-5, 10))

            trend = "↑" if pred > final else ("↓" if pred < final else "→")

            now = time.time()

            # Alerts
            if pred > 20 and now - st.session_state.alert_spike[loc] > 5:
                alerts.append(f"⚠ {loc}: Crowd spike expected")
                st.session_state.alert_spike[loc] = now

            if trend == "↑" and pred > final + 5 and now - st.session_state.alert_trend[loc] > 5:
                alerts.append(f"📈 {loc}: Increasing trend")
                st.session_state.alert_trend[loc] = now

            # Heatmap data
            heatmap_data.append({
                "lat": cfg["lat"],
                "lon": cfg["lon"],
                "intensity": final,
                "location": loc
            })

            # UI
            with tiles[i].container():
                st.markdown(f"### {loc}")

                # 🎥 CLOUD SAFE VIDEO
                st.video(cfg["video"])

                c1, c2 = st.columns(2)
                c1.metric("Camera", ai)
                c2.metric("Network", telco)

                st.metric("Current", final)
                st.metric("Prediction", pred)

        # KPIs
        with kpi_placeholder.container():
            k1, k2, k3 = st.columns(3)
            k1.metric("TOTAL", total)
            k2.metric("PEAK", max(st.session_state.counts.values()))
            k3.metric("FORECAST", total + 10)

        # Alerts
        if alerts:
            for alert in list(set(alerts)):
                st.markdown(f'<div class="blink-alert">{alert}</div>', unsafe_allow_html=True)

        # Heatmap
        df = pd.DataFrame(heatmap_data)

        heat = pdk.Layer(
            "HeatmapLayer",
            data=df,
            get_position='[lon, lat]',
            get_weight="intensity",
            radiusPixels=80,
        )

        text = pdk.Layer(
            "TextLayer",
            data=df,
            get_position='[lon, lat]',
            get_text='location',
            get_size=16,
            get_color=[255,255,255],
            get_pixel_offset=[0,-20],
        )

        view = pdk.ViewState(latitude=19.12, longitude=73.05, zoom=11)

        with heatmap_placeholder.container():
            st.pydeck_chart(pdk.Deck(
                layers=[heat, text],
                initial_view_state=view,
                tooltip={"html":"<b>{location}</b><br/>Crowd:{intensity}"}
            ))

        time.sleep(2)
