import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Padel Mexicano", layout="wide")
st.title("🏓 Padel Mexicano Match Manager")

# ----------------------------
# STATE INIT
if "players" not in st.session_state:
    st.session_state.players = []
if "courts" not in st.session_state:
    st.session_state.courts = 2
if "max_score" not in st.session_state:
    st.session_state.max_score = 21
if "current_matches" not in st.session_state:
    st.session_state.current_matches = []
if "match_started" not in st.session_state:
    st.session_state.match_started = False
if "match_results" not in st.session_state:
    st.session_state.match_results = []

# ----------------------------
# SIDEBAR SETUP
with st.sidebar:
    st.header("🔧 Setup")
    names_input = st.text_area("Masukkan nama pemain (1 baris = 1 nama):", height=200)
    court_count = st.selectbox("Jumlah Court", [1, 2])
    score_option = st.selectbox("Max Score", [21, 24, "Custom"])
    score_custom = st.number_input("Skor Custom", min_value=1, max_value=50, value=25) if score_option == "Custom" else None

    if st.button("🎮 Start Match"):
        names = [n.strip() for n in names_input.split("\n") if n.strip()]
        st.session_state.players = names
        st.session_state.courts = court_count
        st.session_state.max_score = score_custom if score_option == "Custom" else int(score_option)
        st.session_state.match_started = True

        # Generate initial matches
        pool = names.copy()
        random.shuffle(pool)
        st.session_state.current_matches = []
        for i in range(st.session_state.courts):
            if len(pool) >= 4:
                st.session_state.current_matches.append(pool[:4])
                pool = pool[4:]

# ----------------------------
# MATCH VIEW + SCORE INPUT
if st.session_state.match_started:
    st.subheader("🎾 Current Matches")

    for i, match in enumerate(st.session_state.current_matches):
        with st.form(f"court_{i}_form"):
            st.markdown(f"### 🏟️ Court {i+1}")
            col1, col2 = st.columns(2)
            col1.text_input("Team A - Player 1", value=match[0], key=f"{i}_a1", disabled=True)
            col1.text_input("Team A - Player 2", value=match[1], key=f"{i}_a2", disabled=True)
            col2.text_input("Team B - Player 1", value=match[2], key=f"{i}_b1", disabled=True)
            col2.text_input("Team B - Player 2", value=match[3], key=f"{i}_b2", disabled=True)

            s1 = st.number_input("Skor Team A", 0, st.session_state.max_score, key=f"{i}_s1")
            s2 = st.number_input("Skor Team B", 0, st.session_state.max_score, key=f"{i}_s2")

            submitted = st.form_submit_button("✅ Submit Score")
            if submitted:
                st.success("Skor berhasil disimpan!")
                st.session_state.match_results.append({
                    "court": f"Court {i+1}",
                    "team_a": [match[0], match[1]],
                    "team_b": [match[2], match[3]],
                    "score_a": s1,
                    "score_b": s2
                })

    # Show submitted results
    if st.session_state.match_results:
        st.subheader("📋 Hasil Pertandingan")
        df = pd.DataFrame([
            {
                "Court": r["court"],
                "Team A": " & ".join(r["team_a"]),
                "Score A": r["score_a"],
                "Score B": r["score_b"],
                "Team B": " & ".join(r["team_b"]),
            } for r in st.session_state.match_results
        ])
        st.dataframe(df, use_container_width=True)
else:
    st.info("Masukkan nama pemain dan tekan 'Start Match' di sidebar.")
