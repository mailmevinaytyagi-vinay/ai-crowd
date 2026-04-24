import streamlit as st
import cv2
import time
import pandas as pd
import pydeck as pdk

from counter import process_frame
from telecom import get_telecom_estimate, fuse_counts
from prediction import predict_crowd

st.set_page_config(page_title="Crowd Intelligence NOC", layout="wide")

# 🔥 CLEAN DARK UI CSS (SAFE VERSION)
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0E1117;
}

/* Force white text */
html, body, [class*="css"] {
    color: white !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: #1E222A;
    padding: 12px;
    border-radius: 12px;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: #AAAAAA !important;
}

/* Buttons */
div.stButton > button {
    background-color: #2E86FF !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 8px 16px !important;
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
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 6px;
    font-weight: bold;
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
    st.session_state.counts = {loc: 0 for loc in LOCATIONS}

if "history" not in st.session_state:
    st.session_state.history = {loc: [] for loc in LOCATIONS}

if "alert_time_spike" not in st.session_state:
    st.session_state.alert_time_spike = {loc: 0 for loc in LOCATIONS}

if "alert_time_trend" not in st.session_state:
    st.session_state.alert_time_trend = {loc: 0 for loc in LOCATIONS}

# Controls
c1, c2 = st.columns(2)
if c1.button("▶ START"):
    st.session_state.run = True
if c2.button("⏹ STOP"):
    st.session_state.run = False

kpi_placeholder = st.empty()

# Tiles
cols = st.columns(3)
tiles = [cols[0].empty(), cols[1].empty(), cols[2].empty()]

# Heatmap bottom
st.markdown("---")
st.subheader("🗺️ Crowd Heatmap")
heatmap_placeholder = st.empty()

video_caps = {}

if st.session_state.run:

    for loc in LOCATIONS:
        video_caps[loc] = cv2.VideoCapture(LOCATIONS[loc]["video"])

    frame_count = 0

    while True:

        if not st.session_state.run:
            time.sleep(0.2)
            continue

        total = 0
        alerts = []
        heatmap_data = []

        frame_count += 1

        for i, (loc, cfg) in enumerate(LOCATIONS.items()):

            cap = video_caps[loc]
            ret, frame = cap.read()

            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame = cv2.resize(frame, (400, 250))

            if frame_count % 5 == 0:
                _, ai = process_frame(frame)
                st.session_state.counts[loc] = ai

            ai = st.session_state.counts[loc]

            telco, conf = get_telecom_estimate(loc, ai)
            final = fuse_counts(ai, telco)

            # smoothing
            prev = st.session_state.counts[loc]
            final = int(prev * 0.7 + final * 0.3)
            st.session_state.counts[loc] = final

            total += final

            if frame_count % 10 == 0:
                st.session_state.history[loc].append(final)

            pred, pconf, trend = predict_crowd(st.session_state.history[loc])

            now = time.time()

            # ✅ DEMO-FRIENDLY ALERTS
            if pred > 20:
                last = st.session_state.alert_time_spike[loc]
                if now - last > 5:
                    alerts.append(f"⚠ {loc}: Crowd spike expected")
                    st.session_state.alert_time_spike[loc] = now

            if trend == "↑" and pred > final + 5:
                last = st.session_state.alert_time_trend[loc]
                if now - last > 5:
                    alerts.append(f"📈 {loc}: Increasing trend")
                    st.session_state.alert_time_trend[loc] = now

            heatmap_data.append({
                "lat": cfg["lat"],
                "lon": cfg["lon"],
                "intensity": final,
                "location": loc
            })

            trend_icon = "↑" if trend=="↑" else ("↓" if trend=="↓" else "→")

            with tiles[i].container():
                st.markdown(f"### {loc}")
                st.image(frame, channels="BGR")

                a,b = st.columns(2)
                a.metric("Camera", ai)
                b.metric("Network", telco)

                st.metric("Current", final, delta=trend_icon)
                st.metric("Prediction", pred)

                st.caption(f"Conf:{int(conf*100)}% | Pred:{pconf}")

        # KPI
        total_pred = sum(predict_crowd(st.session_state.history[l])[0] for l in LOCATIONS)

        with kpi_placeholder.container():
            k1,k2,k3 = st.columns(3)
            k1.metric("TOTAL", total)
            k2.metric("PEAK", max(st.session_state.counts.values()))
            k3.metric("FORECAST", total_pred)

        # 🔴 BLINKING ALERTS
        if alerts:
            for alert in list(set(alerts)):
                st.markdown(f'<div class="blink-alert">{alert}</div>', unsafe_allow_html=True)

        # 🗺️ HEATMAP (SCROLL + ZOOM ENABLED)
        if frame_count % 10 == 0:

            df = pd.DataFrame(heatmap_data)

            heat = pdk.Layer(
                "HeatmapLayer",
                data=df,
                get_position='[lon, lat]',
                get_weight="intensity",
                radiusPixels=80,
            )

            scatter = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[lon, lat]',
                get_radius=100,
                get_fill_color=[255, 80, 80],
            )

            text = pdk.Layer(
                "TextLayer",
                data=df,
                get_position='[lon, lat]',
                get_text='location',
                get_size=18,
                get_color=[255,255,255],
                get_pixel_offset=[0,-20],
            )

            view = pdk.ViewState(latitude=19.12, longitude=73.05, zoom=11)

            with heatmap_placeholder.container():
                st.pydeck_chart(pdk.Deck(
                    layers=[heat, scatter, text],
                    initial_view_state=view,
                    tooltip={"html":"<b>{location}</b><br/>Crowd:{intensity}"}
                ))

        time.sleep(0.05)