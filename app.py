import streamlit as st
import matplotlib.pyplot as plt
from clean_structured_analysis import (
    load_data,
    apply_timeline,
    convert_coordinates,
    separate_events,
    plot_journey,
    plot_heatmaps
)

# -------------------------------------------------------
# PAGE SETUP
# -------------------------------------------------------
# st.set_page_config(layout="wide")
st.title("🎮 Player Telemetry Dashboard")

# -------------------------------------------------------
# STEP 1: LOAD DATA
# -------------------------------------------------------
df = load_data()

# -------------------------------------------------------
# STEP 2: SIDEBAR FILTERS
# -------------------------------------------------------
st.sidebar.header("Filters")

# Map filter - available maps show aagum
selected_map = st.sidebar.selectbox("Select Map", df["map_id"].unique())

# Match filter - selected map la matches show aagum
map_df = df[df["map_id"] == selected_map]
selected_match = st.sidebar.selectbox("Select Match", map_df["match_id"].unique())

# Date filter - selected match la dates show aagum
match_df = map_df[map_df["match_id"] == selected_match]
available_dates = match_df["ts"].dt.date.unique()
selected_date = st.sidebar.selectbox("Select Date", available_dates)

# Timeline slider - seconds adjust pannalam
timeline_seconds = st.sidebar.slider("Timeline (seconds)", 5, 300, 60)

# -------------------------------------------------------
# STEP 3: FILTER DATA
# -------------------------------------------------------
df = df[df["map_id"] == selected_map]
df = df[df["match_id"] == selected_match]
df = df[df["ts"].dt.date == selected_date]
df = apply_timeline(df, seconds=timeline_seconds)

# -------------------------------------------------------
# STEP 4: CONVERT COORDINATES
# -------------------------------------------------------
df = convert_coordinates(df)

# -------------------------------------------------------
# STEP 5: SEPARATE EVENTS
# -------------------------------------------------------
human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df = separate_events(df)

# -------------------------------------------------------
# STEP 6: CHECK DATA
# -------------------------------------------------------
if len(human_df) == 0:
    st.warning("⚠️ No player data for this selection. Try increasing the timeline or changing filters.")
    st.stop()

# -------------------------------------------------------
# STEP 7: SHOW PLAYER JOURNEY
# -------------------------------------------------------
st.subheader("🗺️ Player Journey")

plot_journey(human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df)
st.pyplot(plt.gcf())
plt.close()

# -------------------------------------------------------
# STEP 8: SHOW HEATMAPS
# -------------------------------------------------------
st.subheader("🔥 Heatmaps")

fig_h1, fig_h2, fig_h3 = plot_heatmaps(human_df, kill_df, botkill_df, death_df, botdeath_df)

col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(fig_h1)
    plt.close()

with col2:
    st.pyplot(fig_h2)
    plt.close()

with col3:
    st.pyplot(fig_h3)
    plt.close()