import streamlit as st
import pandas as pd

st.set_page_config(page_title="Padel Mexicano Tracker", layout="centered")

st.title("🏓 Padel Mexicano Score Tracker")

# Settings
st.sidebar.header("Match Settings")
num_players = st.sidebar.slider("Number of Players", 4, 20, 8, step=2)
num_courts = st.sidebar.selectbox("Number of Courts", [1, 2])

# Initialize match data
if "matches" not in st.session_state:
    st.session_state.matches = []

st.subheader("📝 Input Match Result")
with st.form("match_form"):
    players = [f"Player {i+1}" for i in range(num_players)]
    
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.selectbox("Team 1 - Player A", players, key="p1")
        p2 = st.selectbox("Team 1 - Player B", [p for p in players if p != p1], key="p2")
    with col2:
        p3 = st.selectbox("Team 2 - Player C", [p for p in players if p not in [p1, p2]], key="p3")
        p4 = st.selectbox("Team 2 - Player D", [p for p in players if p not in [p1, p2, p3]], key="p4")

    s1 = st.number_input("Score Team 1", 0, 21, value=0, key="score1")
    s2 = st.number_input("Score Team 2", 0, 21, value=0, key="score2")

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.matches.append({
            "Team 1": [p1, p2],
            "Team 2": [p3, p4],
            "Score T1": s1,
            "Score T2": s2
        })
        st.success("Match result submitted!")

# Leaderboard
st.subheader("📊 Leaderboard")
scores = {p: 0 for p in players}
for match in st.session_state.matches:
    winners = []
    if match["Score T1"] > match["Score T2"]:
        winners = match["Team 1"]
    elif match["Score T2"] > match["Score T1"]:
        winners = match["Team 2"]
    for w in winners:
        scores[w] += 1

df = pd.DataFrame(list(scores.items()), columns=["Player", "Points"])
df = df.sort_values("Points", ascending=False).reset_index(drop=True)
st.table(df)
