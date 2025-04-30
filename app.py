import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Padel Mexicano (Dynamic)", layout="wide")
st.title("🏓 Padel Mexicano - Dynamic Court Rotation")

# -----------------------------
# Session State Initialization
if "players" not in st.session_state:
    st.session_state.players = {}
if "matches" not in st.session_state:
    st.session_state.matches = {}
if "results" not in st.session_state:
    st.session_state.results = []
if "max_score" not in st.session_state:
    st.session_state.max_score = 21
if "courts" not in st.session_state:
    st.session_state.courts = 2
if "submitted_scores" not in st.session_state:
    st.session_state.submitted_scores = {}
if "score_inputs" not in st.session_state:
    st.session_state.score_inputs = {}

# -----------------------------
# Sidebar Configuration
with st.sidebar:
    st.header("🔧 Setup")
    names_input = st.text_area("Masukkan nama pemain (1 baris = 1 nama):", height=200)
    court_count = st.selectbox("Jumlah Court", [1, 2])
    score_option = st.selectbox("Max Score", [21, 24, "Custom"])
    custom_score = st.number_input("Skor Custom", 1, 50, value=25) if score_option == "Custom" else None
    start_button = st.button("🚀 Mulai Permainan")

    if start_button:
        names = [n.strip() for n in names_input.split("\n") if n.strip()]
        if len(names) < 4:
            st.warning("Minimal 4 pemain dibutuhkan.")
        else:
            st.session_state.players = {name: {"points": 0, "playing": False} for name in names}
            st.session_state.matches = {}
            st.session_state.results = []
            st.session_state.submitted_scores = {}
            st.session_state.score_inputs = {}
            st.session_state.max_score = custom_score if score_option == "Custom" else int(score_option)
            st.session_state.courts = court_count

# -----------------------------
# Helper Functions
def get_next_match():
    free_players = [p for p, v in st.session_state.players.items() if not v["playing"]]
    if len(free_players) < 4:
        return None
    sorted_players = sorted(free_players, key=lambda p: st.session_state.players[p]["points"])
    return sorted_players[:4]

def assign_new_match(court_key):
    match = get_next_match()
    if match:
        for p in match:
            st.session_state.players[p]["playing"] = True
        st.session_state.matches[court_key] = match
        st.session_state.score_inputs[court_key] = 0
    else:
        st.session_state.matches[court_key] = None

# -----------------------------
# Initial Match Assignment
for court_id in range(1, st.session_state.courts + 1):
    court_key = f"court_{court_id}"
    if court_key not in st.session_state.matches or st.session_state.matches[court_key] is None:
        assign_new_match(court_key)

# -----------------------------
# Display Courts and Forms
updated_courts = []

for court_id in range(1, st.session_state.courts + 1):
    court_key = f"court_{court_id}"
    match = st.session_state.matches.get(court_key)
    st.subheader(f"🏟️ Court {court_id}")

    if match:
        col1, col2 = st.columns(2)
        col1.markdown(f"**Team A**: `{match[0]}` & `{match[1]}`")
        col2.markdown(f"**Team B**: `{match[2]}` & `{match[3]}`")

        with st.form(f"form_{court_key}", clear_on_submit=False):
            score_a = st.slider("Skor Team A", 0, st.session_state.max_score,
                                st.session_state.score_inputs.get(court_key, 0),
                                key=f"slider_{court_key}")
            score_b = st.session_state.max_score - score_a
            st.session_state.score_inputs[court_key] = score_a

            st.markdown(f"### 🎯 Skor Saat Ini:")
            st.markdown(f"- Team A: `{score_a}`")
            st.markdown(f"- Team B: `{score_b}`")

            submitted = st.form_submit_button("✅ Submit Score")

            if submitted:
                result = {
                    "Court": court_id,
                    "Team A": f"{match[0]} & {match[1]}",
                    "Score A": score_a,
                    "Score B": score_b,
                    "Team B": f"{match[2]} & {match[3]}"
                }
                st.session_state.results.append(result)

                if score_a > score_b:
                    st.session_state.players[match[0]]["points"] += 1
                    st.session_state.players[match[1]]["points"] += 1
                elif score_b > score_a:
                    st.session_state.players[match[2]]["points"] += 1
                    st.session_state.players[match[3]]["points"] += 1

                for p in match:
                    st.session_state.players[p]["playing"] = False

                st.session_state.submitted_scores[court_key] = True
                updated_courts.append(court_key)

# -----------------------------
# Update Courts After Score Submission
for court_key in updated_courts:
    assign_new_match(court_key)
    st.session_state.submitted_scores.pop(court_key, None)

# -----------------------------
# Show Resting Players
free_players = [p for p, v in st.session_state.players.items() if not v["playing"]]
if free_players:
    st.subheader("😌 Pemain yang sedang istirahat:")
    st.write(", ".join(free_players))

# -----------------------------
# Results Table
if st.session_state.results:
    st.subheader("📋 Hasil Pertandingan")
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df, use_container_width=True)

# -----------------------------
# Leaderboard
if st.session_state.players:
    st.subheader("🏆 Leaderboard")
    leaderboard = sorted(st.session_state.players.items(), key=lambda x: x[1]["points"], reverse=True)
    lb_df = pd.DataFrame([{"Pemain": k, "Poin": v["points"]} for k, v in leaderboard])
    st.dataframe(lb_df, use_container_width=True)
