import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Nationals Pitching Decision Support Tool",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("Controls")

screen_type = st.sidebar.radio(
    "Candidate Screen",
    ["Immediate Impact", "Development / Upside"]
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Prototype built from public Statcast data "
    "and manually researched roster/context information."
)

# -----------------------------
# HEADER
# -----------------------------

st.title("Nationals Pitching Decision Support Tool")
st.caption(
    "Prototype for diagnosing Washington's bullpen needs "
    "and identifying potential pitching targets."
)

st.markdown("---")

# -----------------------------
# SECTION 1: TEAM DIAGNOSTIC
# -----------------------------

st.header("Nationals Bullpen Diagnostic")

st.write(
    "April–August 2026 public Statcast sample. "
    "Metrics below compare Washington's bullpen against MLB."
)

metrics = {
    "Avg Fastball Velocity": "93.9 mph",
    "Fastball Whiff Rate": "14.5%",
    "Overall Whiff Rate": "20.9%",
    "Strikeout Rate": "19.0%",
    "Walk Rate": "9.8%",
    "Hard-Hit Rate": "24.6%"
}

cols = st.columns(3)

for i, (label, value) in enumerate(metrics.items()):
    with cols[i % 3]:
        st.metric(label, value)

st.subheader("MLB Relative Position")

rank_data = pd.DataFrame({
    "Metric": [
        "Primary Fastball Velocity",
        "Fastball Whiff Rate",
        "Overall Whiff Rate"
    ],
    "WSH Rank": [
        "25th of 30",
        "26th of 30",
        "30th of 30"
    ]
})

st.dataframe(
    rank_data,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Prototype finding: Washington's bullpen weakness is broader than raw velocity alone. "
    "The data suggests a need for pitchers who add swing-and-miss ability while maintaining "
    "acceptable control and contact suppression."
)

st.markdown("---")

# -----------------------------
# SECTION 2: CANDIDATE SCREEN
# -----------------------------

st.header("Candidate Screen")

st.caption(
    "Use the sidebar to switch between immediate-impact and development/upside profiles."
)

immediate_impact = pd.DataFrame([
    ["Sommers, Drew", "DET", 95.0, 29.0, 29.5, 37.7, 8.2, 14.3],
    ["Montgomery, Mason", "PIT", 98.7, 27.3, 29.4, 39.4, 7.3, 20.4],
    ["Bowlan, Jonathan", "PHI", 97.1, 26.9, 28.9, 31.8, 7.3, 19.8],
    ["Fuentes, Didier", "ATL", 97.3, 24.2, 27.2, 30.7, 7.0, 17.1],
    ["Morillo, Juan", "AZ", 98.7, 23.8, 27.1, 29.0, 8.1, 17.6]
], columns=[
    "Player",
    "Team",
    "Avg Fastball Velocity",
    "Fastball Whiff %",
    "Overall Whiff %",
    "K %",
    "BB %",
    "Hard-Hit %"
])

upside = pd.DataFrame([
    ["Miller, Erik", "BOS", 96.9, 15.4, 34.7, 35.2, 12.5, 17.3],
    ["Hurt, Kyle", "LAD", 96.6, 28.0, 32.5, 29.5, 11.9, 23.5],
    ["Zeferjahn, Ryan", "CHC", 97.1, 25.8, 30.1, 31.5, 11.9, 22.4],
    ["Mey, Luis", "CIN", 98.3, 25.6, 31.0, 31.7, 14.4, 24.0],
    ["Henriquez, Edgardo", "LAD", 100.7, 21.6, 28.2, 28.6, 10.8, 15.4]
], columns=[
    "Player",
    "Team",
    "Avg Fastball Velocity",
    "Fastball Whiff %",
    "Overall Whiff %",
    "K %",
    "BB %",
    "Hard-Hit %"
])

if screen_type == "Immediate Impact":
    display_df = immediate_impact
else:
    display_df = upside

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# -----------------------------
# SECTION 3: FINAL SHORTLIST
# -----------------------------

st.header("Final Shortlist")

final_shortlist = pd.DataFrame([
    [
        "Montgomery, Mason",
        "PIT",
        "Premium Immediate Impact",
        98.7,
        29.4,
        39.4,
        7.3,
        "Young, controllable high-leverage left-hander; likely expensive in trade.",
        "Premium velocity, elite strikeout rate, strong whiffs, and better-than-WSH control."
    ],
    [
        "Sommers, Drew",
        "DET",
        "Immediate Impact",
        95.0,
        29.5,
        37.7,
        8.2,
        "Young, controllable left-hander; strong performance likely raises acquisition cost.",
        "Adds major swing-and-miss and strikeout gains without relying solely on velocity."
    ],
    [
        "Bowlan, Jonathan",
        "PHI",
        "Immediate Impact",
        97.1,
        28.9,
        31.8,
        7.3,
        "Controllable setup reliever; current groin issue requires medical follow-up.",
        "Adds velocity, whiffs, strikeouts, control, and contact suppression versus WSH baseline."
    ],
    [
        "Hurt, Kyle",
        "LAD",
        "Development / Upside",
        96.6,
        32.5,
        29.5,
        11.9,
        "Has been optioned repeatedly; control remains the main development risk.",
        "Strong velocity and bat-missing ability with a potentially improvable control weakness."
    ],
    [
        "Henriquez, Edgardo",
        "LAD",
        "Extreme-Velocity Upside",
        100.7,
        28.2,
        28.6,
        10.8,
        "Young, controllable power arm; current back issue adds medical uncertainty.",
        "Extreme velocity directly addresses WSH's velocity gap while adding swing-and-miss upside."
    ]
], columns=[
    "Player",
    "Team",
    "Profile",
    "Avg FB Velo",
    "Overall Whiff %",
    "K %",
    "BB %",
    "Context",
    "Why He Fits WSH"
])

st.dataframe(
    final_shortlist,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Shortlist inclusion indicates a player merits deeper scouting, roster, medical, "
    "and acquisition analysis. It is not an acquisition recommendation."
)

st.markdown("---")

# -----------------------------
# SECTION 4: PLAYER DETAIL
# -----------------------------

st.header("Player Detail")

player_choice = st.selectbox(
    "Select a shortlisted pitcher:",
    final_shortlist["Player"].tolist()
)

selected_player = final_shortlist[
    final_shortlist["Player"] == player_choice
].iloc[0]

st.subheader(player_choice)

detail_cols = st.columns(4)

with detail_cols[0]:
    st.metric(
        "Avg Fastball Velocity",
        f"{selected_player['Avg FB Velo']:.1f} mph",
        f"{selected_player['Avg FB Velo'] - 93.9:+.1f} vs WSH"
    )

with detail_cols[1]:
    st.metric(
        "Overall Whiff Rate",
        f"{selected_player['Overall Whiff %']:.1f}%",
        f"{selected_player['Overall Whiff %'] - 20.9:+.1f} pts vs WSH"
    )

with detail_cols[2]:
    st.metric(
        "Strikeout Rate",
        f"{selected_player['K %']:.1f}%",
        f"{selected_player['K %'] - 19.0:+.1f} pts vs WSH"
    )

with detail_cols[3]:
    st.metric(
        "Walk Rate",
        f"{selected_player['BB %']:.1f}%",
        f"{selected_player['BB %'] - 9.8:+.1f} pts vs WSH",
        delta_color="inverse"
    )

st.markdown(f"**Profile:** {selected_player['Profile']}")
st.markdown(f"**Context:** {selected_player['Context']}")
st.markdown(f"**Why He Fits WSH:** {selected_player['Why He Fits WSH']}")

st.subheader("WSH vs Selected Pitcher")

indexed_comparison = pd.DataFrame({
    "Metric": [
        "Fastball Velocity",
        "Overall Whiff",
        "Strikeout Rate",
        "Walk Control"
    ],
    "WSH Bullpen": [
        100,
        100,
        100,
        100
    ],
    player_choice: [
        selected_player["Avg FB Velo"] / 93.9 * 100,
        selected_player["Overall Whiff %"] / 20.9 * 100,
        selected_player["K %"] / 19.0 * 100,
        9.8 / selected_player["BB %"] * 100
    ]
})

chart_data = indexed_comparison.melt(
    id_vars="Metric",
    var_name="Pitcher",
    value_name="Index"
)

chart = (
    alt.Chart(chart_data)
    .mark_bar()
    .encode(
        x=alt.X(
            "Metric:N",
            title=None,
            sort=[
                "Fastball Velocity",
                "Overall Whiff",
                "Strikeout Rate",
                "Walk Control"
            ]
        ),
        y=alt.Y(
            "Index:Q",
            title="Index (WSH = 100)"
        ),
        xOffset="Pitcher:N",
        color=alt.Color(
            "Pitcher:N",
            title=None
        ),
        tooltip=[
            "Pitcher:N",
            "Metric:N",
            alt.Tooltip("Index:Q", format=".0f")
        ]
    )
    .properties(height=400)
)

st.altair_chart(
    chart,
    use_container_width=True
)

st.caption(
    "Indexed to the Washington bullpen baseline (100). "
    "Values above 100 indicate improvement relative to WSH. "
    "Walk rate is inverted because lower BB% is better."
)

st.markdown("---")

# -----------------------------
# SECTION 5: METHODOLOGY
# -----------------------------

with st.expander("Methodology & Data Notes"):
    st.markdown(
        """
        **Analysis period:** April 1 through August 31, 2026.

        **Primary data source:** Public MLB Statcast data accessed through `pybaseball`.

        **Reliever identification:** Pitchers were classified as relievers when their first
        appearance in a game occurred after the first inning. This is a practical MVP rule
        and does not perfectly distinguish openers or unusual bullpen usage.

        **Primary fastballs:** Four-seam fastballs and sinkers were used for the primary
        fastball velocity and fastball whiff analysis.

        **Whiff rate:** Swinging strikes divided by total swings.

        **Candidate screens:** Transparent thresholds were used rather than a composite
        opportunity score so that analysts can see why each pitcher surfaced.

        **Context layer:** Current organization, roster/contract status, transactions,
        and injury notes were researched separately from the Statcast performance sample.

        **Important limitation:** This prototype is a decision-support tool for deeper
        scouting and acquisition research. It does not estimate trade value, predict future
        performance, or replace scouting, medical, or player-development evaluation.
        """
    )
