import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Padel Mexicano Manager", layout="wide")
st.title("🏓 Padel Mexicano Match Manager")

# -------------------------------
# STATE INIT
if "players" not in st.session_state:
    st.session_state.players = []
if "courts" not in st.session_state:
    st.session_state.courts = 2
if "max_score" not in st.session_state:
    st.session_state.max_score = 21
if "matches_played" not in st.session_state:
    st.session_state.matches_played = []
if "current_matches" not in st.session_state:
    st.session_state.current_matches = []
if "match_started" not in st.session_state:
    st.session_state.match_started = False

# -------------------------------
# INPUT
with st.sidebar:
    st.header("🔧 Setup")
    names_input = st.text_area("Masukkan nama pemain (1 baris = 1 nama):", height=200)
    court_count = st.selectbox("Jumlah Court", [1, 2])
    score_option = st.selectbox("Max Score", [21, 24, "Custom"])
    score_custom = st.number_input("Skor Custom", min_value=1, max_value=50, value=25) if score_option == "Custom" else None

    if st.button("🎮 Start Match"):
        st.session_state.players = [n.strip() for n in names_input.split("\n") if n.strip()]
        st.session_state.courts = court_count
        st.session_state.max_score = score_custom if score_option == "Custom" else int(score_option)
        st.session_state.match_started = True

        # generate initial matches
        all_players = st.session_state.players.copy()
        random.shuffle(all_players)
        st.session_state.current_matches = []
        for i in range(st.session_state.courts):
            if len(all_players) >= 4:
                match_players = all_players[:4]
                st.session_state.current_matches.append(match_players)
                all_players = all_players[4:]

# -------------------------------
# DISPLAY COURTS
if st.session_state.match_started:
    st.subheader("🎾 Current Court Matches")
    for i, match in enumerate(st.session_state.current_matches):
        with st.container():
            st.markdown(f"### 🏟️ Court {i+1}")
            cols = st.columns(2)
            cols[0].markdown(f"**Team A**: {match[0]} & {match[1]}")
            cols[1].markdown(f"**Team B**: {match[2]} & {match[3]}")
            st.markdown("---")
else:
    st.info("Silakan isi nama pemain dan tekan 'Start Match' di sidebar.")
