# Preparing the full source code of a Streamlit app based on the user's specification

app_code = '''
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Padel Mexicano Match Manager", layout="wide")
st.title("🏓 Padel Mexicano Match Manager")

# Session State Initialization
if "players" not in st.session_state:
    st.session_state.players = []
if "courts" not in st.session_state:
    st.session_state.courts = 1
if "max_score" not in st.session_state:
    st.session_state.max_score = 21
if "matches_played" not in st.session_state:
    st.session_state.matches_played = []
if "current_matches" not in st.session_state:
    st.session_state.current_matches = []

# Input Section
with st.sidebar:
    st.header("🔧 Match Setup")
    player_input = st.text_area("Enter player names (one per line):")
    court_count = st.selectbox("Number of Courts", [1, 2], index=1)
    score_type = st.selectbox("Max Score", [21, 24, "Custom"])
    custom_score = st.number_input("Custom Score", min_value=1, max_value=50, value=21) if score_type == "Custom" else None
    if st.button("Start Match"):
        st.session_state.players = [p.strip() for p in player_input.strip().split("\\n") if p.strip()]
        st.session_state.courts = court_count
        st.session_state.max_score = custom_score if score_type == "Custom" else int(score_type)
        st.session_state.matches_played = []
        st.session_state.current_matches = []

        # Generate initial matches
        random.shuffle(st.session_state.players)
        for c in range(st.session_state.courts):
            if len(st.session_state.players) >= 4:
                match_players = st.session_state.players[:4]
                st.session_state.current_matches.append(match_players)
                st.session_state.players = st.session_state.players[4:]

# Show current matches
st.subheader("🎾 Current Matches")
for i, match in enumerate(st.session_state.current_matches):
    with st.container():
        st.markdown(f"**Court {i+1}**")
        team1 = st.text_input(f"Court {i+1} - Player 1", value=match[0], key=f"c{i}p1")
        team2 = st.text_input(f"Court {i+1} - Player 2", value=match[1], key=f"c{i}p2")
        team3 = st.text_input(f"Court {i+1} - Player 3", value=match[2], key=f"c{i}p3")
        team4 = st.text_input(f"Court {i+1} - Player 4", value=match[3], key=f"c{i}p4")
        st.markdown("---")

# Simulate next round logic (simple logic: shuffle remaining and rotate losers)
if st.button("➡️ Next Round"):
    # Flatten all current match players into the back of the player list (simulate all played)
    for match in st.session_state.current_matches:
        st.session_state.players.extend(match)

    random.shuffle(st.session_state.players)
    st.session_state.current_matches = []
    for c in range(st.session_state.courts):
        if len(st.session_state.players) >= 4:
            match_players = st.session_state.players[:4]
            st.session_state.current_matches.append(match_players)
            st.session_state.players = st.session_state.players[4:]
'''

