import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="Minecraft Wrapped",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── THEME & CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        background-color: #080c10 !important;
        color: #e0e0e0;
    }
    .main { background-color: #080c10; }
    .block-container { padding: 2rem 3rem; max-width: 1400px; }

    /* HERO */
    .hero {
        text-align: center;
        padding: 3rem 0 2rem 0;
        position: relative;
    }
    .hero-title {
        font-family: 'Press Start 2P', monospace;
        font-size: 2.2rem;
        color: #5dff8a;
        text-shadow: 0 0 20px #5dff8a66, 0 0 40px #5dff8a33;
        line-height: 1.6;
        letter-spacing: 2px;
    }
    .hero-sub {
        font-family: 'Inter', sans-serif;
        color: #666;
        font-size: 1rem;
        margin-top: 1rem;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    /* CARDS */
    .stat-card {
        background: linear-gradient(145deg, #0d1117, #111827);
        border: 1px solid #1e2d3d;
        border-radius: 16px;
        padding: 24px 16px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #5dff8a, #00d4ff);
    }
    .stat-number {
        font-family: 'Press Start 2P', monospace;
        font-size: 1.4rem;
        color: #5dff8a;
        margin: 8px 0 4px 0;
        text-shadow: 0 0 12px #5dff8a55;
    }
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
    }
    .stat-emoji { font-size: 1.6rem; }

    /* SECTION HEADERS */
    .section-header {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.9rem;
        color: #5dff8a;
        letter-spacing: 2px;
        padding: 12px 0 8px 0;
        border-bottom: 1px solid #1e2d3d;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 10px #5dff8a44;
    }

    /* PLAYSTYLE */
    .playstyle-wrap {
        background: linear-gradient(135deg, #0d1117, #0a1628);
        border: 1px solid #1e4060;
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .playstyle-wrap::after {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at center, #5dff8a0a 0%, transparent 70%);
        pointer-events: none;
    }
    .playstyle-title {
        font-family: 'Press Start 2P', monospace;
        font-size: 1.1rem;
        color: #5dff8a;
        margin: 12px 0 8px 0;
        text-shadow: 0 0 16px #5dff8a66;
    }
    .playstyle-desc {
        font-family: 'Inter', sans-serif;
        color: #8899aa;
        font-style: italic;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* INFO CARDS */
    .info-card {
        background: #0d1117;
        border: 1px solid #1e2d3d;
        border-left: 3px solid #5dff8a;
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin: 8px 0;
        font-family: 'Inter', sans-serif;
    }
    .info-label {
        font-size: 0.7rem;
        color: #5dff8a;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    .info-value {
        font-size: 1rem;
        color: #e0e0e0;
        margin: 4px 0 0 0;
    }
    .info-sub {
        font-size: 0.75rem;
        color: #556;
        margin: 2px 0 0 0;
    }

    /* TRAUMA CARD */
    .trauma-card {
        background: linear-gradient(135deg, #1a0808, #0d1117);
        border: 1px solid #3d1e1e;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        font-family: 'Inter', sans-serif;
    }

    /* AI SECTION */
    .ai-section {
        background: linear-gradient(135deg, #0a0d1a, #0d1117);
        border: 1px solid #1e2d5a;
        border-radius: 20px;
        padding: 32px;
        margin: 16px 0;
        position: relative;
        overflow: hidden;
    }
    .ai-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #7c3aed, #2563eb, #5dff8a);
    }
    .ai-output {
        background: #080c10;
        border: 1px solid #1e2d3d;
        border-radius: 12px;
        padding: 24px;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        line-height: 1.8;
        color: #cdd5e0;
        margin-top: 16px;
        white-space: pre-wrap;
    }
    .ai-tab-header {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.7rem;
        color: #7c3aed;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    /* ORE BARS */
    .ore-bar {
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        margin: 4px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Inter', sans-serif;
    }

    /* UPLOAD ZONE */
    .upload-zone {
        background: #0d1117;
        border: 2px dashed #1e2d3d;
        border-radius: 20px;
        padding: 60px;
        text-align: center;
        margin: 2rem 0;
    }
    .upload-title {
        font-family: 'Press Start 2P', monospace;
        font-size: 1rem;
        color: #5dff8a;
        margin: 1rem 0 0.5rem 0;
    }
    .upload-sub {
        font-family: 'Inter', sans-serif;
        color: #556;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    code {
        background: #0a0f1a !important;
        color: #5dff8a !important;
        border: 1px solid #1e2d3d !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        font-size: 0.8rem !important;
    }

    /* STREAMLIT OVERRIDES */
    .stButton > button {
        background: linear-gradient(135deg, #5dff8a, #00d4ff) !important;
        color: #080c10 !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 0.6rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        letter-spacing: 1px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px #5dff8a44 !important;
    }
    .stFileUploader { border-radius: 12px; }
    .stTextInput > div > div > input {
        background: #0d1117 !important;
        border: 1px solid #1e2d3d !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stTabs"] button {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        color: #556 !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #5dff8a !important;
        border-bottom-color: #5dff8a !important;
    }
    .stSpinner > div { border-top-color: #5dff8a !important; }

    /* DIVIDER */
    hr { border-color: #1e2d3d !important; margin: 2rem 0 !important; }

    /* FOOTER */
    .footer {
        text-align: center;
        padding: 2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #333;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ───
def load_stats(file):
    data = json.load(file)
    return data.get("stats", {})

def clean(name):
    return name.replace("minecraft:", "").replace("_", " ").title()

def cm_to_km(cm): return round(cm / 100000, 2)
def ticks_to_hours(t): return round(t / 20 / 3600, 2)

def get_playstyle(stats):
    mined    = stats.get("minecraft:mined", {})
    killed   = stats.get("minecraft:killed", {})
    custom   = stats.get("minecraft:custom", {})
    crafted  = stats.get("minecraft:crafted", {})

    scores = {
        ("⛏️", "THE MINER",    "You live underground. Stone is your carpet. Diamonds are your religion. Surface is for quitters."):
            sum(mined.values()),
        ("⚔️", "THE FIGHTER",  "Everything that moves is a target. You have a kill count that would make generals nervous."):
            sum(killed.values()) * 10,
        ("🏃", "THE EXPLORER", "The horizon is always calling. You have walked more than most people drive in a week."):
            cm_to_km(custom.get("minecraft:sprint_one_cm", 0)) * 100,
        ("🐇", "THE CHAOS AGENT", "You sprint jump everywhere, water bucket off cliffs, and make the laws of physics uncomfortable."):
            custom.get("minecraft:jump", 0) * 5,
        ("🍖", "THE SURVIVOR",  "You farm, you eat, you sleep on time. Practical, methodical, disgustingly efficient."):
            sum(crafted.values()) * 8,
    }
    return max(scores, key=scores.get)

def build_stats_summary(stats):
    mined    = stats.get("minecraft:mined", {})
    killed   = stats.get("minecraft:killed", {})
    killed_by = stats.get("minecraft:killed_by", {})
    crafted  = stats.get("minecraft:crafted", {})
    custom   = stats.get("minecraft:custom", {})

    top_mined   = sorted(mined.items(),    key=lambda x: x[1], reverse=True)[:5]
    top_killed  = sorted(killed.items(),   key=lambda x: x[1], reverse=True)[:5]
    top_crafted = sorted(crafted.items(),  key=lambda x: x[1], reverse=True)[:5]

    return f"""
PLAYER STATS SUMMARY:
- Play time: {ticks_to_hours(custom.get('minecraft:play_time', 0))} hours
- Total blocks mined: {sum(mined.values())}
- Total mobs killed: {sum(killed.values())}
- Deaths: {custom.get('minecraft:deaths', 0)}
- Killed by: {dict(killed_by)}
- Total jumps: {custom.get('minecraft:jump', 0)}
- Sprint distance: {cm_to_km(custom.get('minecraft:sprint_one_cm', 0))} km
- Swim distance: {cm_to_km(custom.get('minecraft:swim_one_cm', 0))} km
- Fly/airborne distance: {cm_to_km(custom.get('minecraft:fly_one_cm', 0))} km
- Damage dealt: {custom.get('minecraft:damage_dealt', 0)}
- Damage taken: {custom.get('minecraft:damage_taken', 0)}
- Top blocks mined: {[(clean(k), v) for k, v in top_mined]}
- Top mobs killed: {[(clean(k), v) for k, v in top_killed]}
- Top items crafted: {[(clean(k), v) for k, v in top_crafted]}
- Animals bred: {custom.get('minecraft:animals_bred', 0)}
- Times slept: {custom.get('minecraft:sleep_in_bed', 0)}
- Fish caught context: Salmon killed = {killed.get('minecraft:salmon', 0)}
""".strip()

def call_claude(api_key, system_prompt, user_prompt):
    client = Groq(api_key=api_key)
    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ]
    )
    return message.choices[0].message.content


# ─── HERO ───
st.markdown("""
<div class="hero">
    <div class="hero-title">⛏ MINECRAFT<br>WRAPPED</div>
    <div class="hero-sub">Your survival story, told in data</div>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR: API KEY ───
with st.sidebar:
    st.markdown("### 🤖 AI Features")
    st.markdown("Add your Groq API key to unlock AI roast, story, coaching and predictions. It is 100% free!")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.markdown("[Get your free API key →](https://console.groq.com)", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**📁 Stats file location:**")
    st.code(".minecraft/saves/\nYourWorld/stats/\nyourfile.json")

# ─── FILE UPLOAD ───
uploaded_file = st.file_uploader("", type="json", label_visibility="collapsed")

if uploaded_file is None:
    st.markdown("""
    <div class="upload-zone">
        <div style="font-size:4rem;">🎮</div>
        <div class="upload-title">UPLOAD YOUR STATS</div>
        <div class="upload-sub">Find your file at:</div>
        <code>C:\\Users\\YourName\\AppData\\Roaming\\.minecraft\\saves\\YourWorld\\stats\\</code>
        <div class="upload-sub" style="margin-top:1rem;">Exit Minecraft with <b>Save and Quit to Title</b> before uploading</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── LOAD DATA ───
stats     = load_stats(uploaded_file)
mined     = stats.get("minecraft:mined", {})
killed    = stats.get("minecraft:killed", {})
killed_by = stats.get("minecraft:killed_by", {})
crafted   = stats.get("minecraft:crafted", {})
custom    = stats.get("minecraft:custom", {})
used      = stats.get("minecraft:used", {})
picked_up = stats.get("minecraft:picked_up", {})

playtime_h   = ticks_to_hours(custom.get("minecraft:play_time", 0))
total_mined  = sum(mined.values())
total_kills  = sum(killed.values())
deaths       = custom.get("minecraft:deaths", 0)
jumps        = custom.get("minecraft:jump", 0)
sprint_km    = cm_to_km(custom.get("minecraft:sprint_one_cm", 0))
swim_km      = cm_to_km(custom.get("minecraft:swim_one_cm", 0))
fly_km       = cm_to_km(custom.get("minecraft:fly_one_cm", 0))
walk_km      = cm_to_km(custom.get("minecraft:walk_one_cm", 0))
fall_km      = cm_to_km(custom.get("minecraft:fall_one_cm", 0))
boat_km      = cm_to_km(custom.get("minecraft:boat_one_cm", 0))
damage_dealt = custom.get("minecraft:damage_dealt", 0)
damage_taken = custom.get("minecraft:damage_taken", 0)
total_dist   = sprint_km + walk_km + swim_km + boat_km

CHART_BG    = "rgba(0,0,0,0)"
GRID_COLOR  = "#1e2d3d"
FONT_COLOR  = "#8899aa"
BASE_LAYOUT = dict(
    paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
    font=dict(color=FONT_COLOR, family="Inter"),
    margin=dict(l=10, r=10, t=40, b=10),
)

st.markdown("---")

# ══════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════
st.markdown('<div class="section-header">📊 &nbsp; OVERVIEW</div>', unsafe_allow_html=True)

cols = st.columns(6)
cards = [
    ("⏱️", f"{playtime_h}h",     "Play Time"),
    ("⛏️", f"{total_mined:,}",   "Blocks Mined"),
    ("⚔️", f"{total_kills:,}",   "Mobs Killed"),
    ("☠️", f"{deaths}",           "Deaths"),
    ("🐇", f"{jumps:,}",          "Total Jumps"),
    ("🏃", f"{round(total_dist , 2)}km",     "Total Distance"),
]
for col, (emoji, number, label) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-emoji">{emoji}</div>
            <div class="stat-number">{number}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# PLAYSTYLE
# ══════════════════════════════════════════════
st.markdown('<div class="section-header">🎭 &nbsp; PLAYSTYLE PROFILE</div>', unsafe_allow_html=True)

ps_emoji, ps_title, ps_desc = get_playstyle(stats)

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"""
    <div class="playstyle-wrap">
        <div style="font-size:4rem;">{ps_emoji}</div>
        <div class="playstyle-title">{ps_title}</div>
        <div class="playstyle-desc">{ps_desc}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    radar_cats = ["Mining", "Combat", "Exploration", "Survival", "Crafting"]
    radar_vals = [
        min(100, total_mined / 5),
        min(100, total_kills / 2),
        min(100, total_dist * 8),
        min(100, max(0, 100 - deaths * 25)),
        min(100, sum(crafted.values()) / 2)
    ]
    fig = go.Figure(go.Scatterpolar(
        r=radar_vals + [radar_vals[0]],
        theta=radar_cats + [radar_cats[0]],
        fill='toself',
        fillcolor='rgba(93,255,138,0.08)',
        line=dict(color='#5dff8a', width=2),
        marker=dict(color='#5dff8a', size=7)
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        polar=dict(
            bgcolor='#0d1117',
            radialaxis=dict(visible=True, range=[0,100], gridcolor=GRID_COLOR, tickfont=dict(color='#444', size=9)),
            angularaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color='#8899aa', size=11))
        ),
        height=280, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════
# MINING
# ══════════════════════════════════════════════
st.markdown('<div class="section-header">⛏️ &nbsp; MINING REPORT</div>', unsafe_allow_html=True)

if mined:
    df_mined = (pd.DataFrame(list(mined.items()), columns=["Block","Count"])
                .assign(Block=lambda d: d.Block.apply(clean))
                .sort_values("Count", ascending=False).head(15))

    col1, col2 = st.columns([3, 1])
    with col1:
        fig = px.bar(df_mined, x="Count", y="Block", orientation="h",
                     color="Count", color_continuous_scale=["#1e3a2f","#5dff8a"])
        fig.update_layout(**BASE_LAYOUT,
            title=dict(text="Top 15 Blocks Mined", font=dict(color="#5dff8a", size=13)),
            xaxis=dict(gridcolor=GRID_COLOR, zeroline=False),
            yaxis=dict(gridcolor=GRID_COLOR, categoryorder="total ascending"),
            coloraxis_showscale=False, height=420
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        ore_keys = ["coal","iron","gold","diamond","lapis","redstone","emerald","copper"]
        ore_colors = {
            "coal":"#666","iron":"#c8a882","gold":"#ffd700","diamond":"#00e5ff",
            "lapis":"#4169e1","redstone":"#ff3333","emerald":"#00ff7f","copper":"#b87333"
        }
        ores_found = {k:v for k,v in mined.items() if any(o in k for o in ore_keys)}
        if ores_found:
            st.markdown("**💎 Ores Found**")
            for ore, count in sorted(ores_found.items(), key=lambda x: x[1], reverse=True):
                clr = next((ore_colors[o] for o in ore_keys if o in ore), "#888")
                st.markdown(f"""
                <div class="ore-bar" style="background: linear-gradient(90deg, {clr}18, #0d1117); border-left: 3px solid {clr};">
                    <span style="color:{clr}; font-weight:600; font-family:Inter;">{clean(ore)}</span>
                    <span style="color:#8899aa; font-family:Inter;">{count}</span>
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════
# COMBAT
# ══════════════════════════════════════════════
st.markdown('<div class="section-header">⚔️ &nbsp; COMBAT REPORT</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if killed:
        df_k = (pd.DataFrame(list(killed.items()), columns=["Mob","Count"])
                .assign(Mob=lambda d: d.Mob.apply(clean))
                .sort_values("Count", ascending=False))
        fig = px.bar(df_k, x="Mob", y="Count",
                     color="Count", color_continuous_scale=["#3a1e1e","#ff6b6b"])
        fig.update_layout(**BASE_LAYOUT,
            title=dict(text="Mobs Killed", font=dict(color="#ff6b6b", size=13)),
            xaxis=dict(gridcolor=GRID_COLOR, tickangle=30),
            yaxis=dict(gridcolor=GRID_COLOR),
            coloraxis_showscale=False, height=340
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if killed_by:
        df_kb = (pd.DataFrame(list(killed_by.items()), columns=["Killer","Count"])
                 .assign(Killer=lambda d: d.Killer.apply(clean)))
        fig = px.pie(df_kb, values="Count", names="Killer",
                     color_discrete_sequence=["#ff6b6b","#ff9f43","#ffd93d","#c0392b"])
        fig.update_layout(**BASE_LAYOUT,
            title=dict(text="Cause of Death", font=dict(color="#ff6b6b", size=13)),
            height=340, showlegend=True,
            legend=dict(font=dict(color="#8899aa"))
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:80px 20px; background:#0d1117; border:1px solid #1e2d3d; border-radius:16px; height:340px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div style="font-size:3rem;">🛡️</div>
            <div style="font-family:'Press Start 2P',monospace; font-size:0.7rem; color:#5dff8a; margin-top:12px;">UNDYING</div>
            <div style="font-family:Inter,sans-serif; color:#556; margin-top:8px; font-size:0.85rem;">Nothing has killed you. Yet.</div>
        </div>
        """, unsafe_allow_html=True)

# Trauma cards
if killed_by:
    st.markdown("**☠️ Death Trauma Report**")
    for killer, count in killed_by.items():
        trauma = min(10, count * 3)
        bar = "💀" * trauma + "⬜" * (10 - trauma)
        st.markdown(f"""
        <div class="trauma-card">
            <b style="color:#ff6b6b; font-family:Inter;">{clean(killer)}</b>
            <span style="color:#556; font-family:Inter;"> — ended you {count} time(s)</span>
            <br><span style="font-size:0.85rem;">{bar} &nbsp; trauma score {trauma}/10</span>
        </div>
        """, unsafe_allow_html=True)

# Damage summary
if damage_dealt or damage_taken:
    col1, col2, col3 = st.columns(3)
    ratio = round(damage_dealt / max(damage_taken, 1), 1)
    with col1:
        st.markdown(f'<div class="info-card"><div class="info-label">Damage Dealt</div><div class="info-value">{damage_dealt:,} HP</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="info-card"><div class="info-label">Damage Taken</div><div class="info-value">{damage_taken:,} HP</div></div>', unsafe_allow_html=True)
    with col3:
        verdict = "Absolute menace 🔥" if ratio > 5 else "Held your ground 💪" if ratio > 2 else "Took some L's 💀"
        st.markdown(f'<div class="info-card"><div class="info-label">Damage Ratio</div><div class="info-value">{ratio}x</div><div class="info-sub">{verdict}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════
# MOVEMENT
# ══════════════════════════════════════════════
st.markdown('<div class="section-header">🗺️ &nbsp; MOVEMENT REPORT</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    move_data = {
        "🏃 Sprint": sprint_km, "✈️ Airborne": fly_km, "🚶 Walk": walk_km,
        "🏊 Swim": swim_km, "⛵ Boat": boat_km, "🤿 Fall": fall_km,
    }
    df_move = (pd.DataFrame(list(move_data.items()), columns=["Type","KM"])
               .query("KM > 0").sort_values("KM", ascending=False))

    fig = px.bar(df_move, x="Type", y="KM",
                 color="KM", color_continuous_scale=["#1e2d4a","#00d4ff"])
    fig.update_layout(**BASE_LAYOUT,
        title=dict(text="Distance by Movement Type (km)", font=dict(color="#00d4ff", size=13)),
        xaxis=dict(gridcolor=GRID_COLOR), yaxis=dict(gridcolor=GRID_COLOR),
        coloraxis_showscale=False, height=320
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    comparisons = [
        ("Total Distance", f"{total_dist} km", f"{round(total_dist/1300*100,1)}% of Kolkata → Delhi"),
        ("Sprint Distance", f"{sprint_km} km", f"Like {round(sprint_km/0.1)} city blocks"),
        ("Swim Distance",   f"{swim_km} km",   f"{round(swim_km*1000)}m underwater"),
        ("Times Jumped",    f"{jumps:,}",       f"~{round(jumps/60)} jumps per minute"),
    ]
    for label, val, sub in comparisons:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">{label}</div>
            <div class="info-value">{val}</div>
            <div class="info-sub">📍 {sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════
# CRAFTING
# ══════════════════════════════════════════════
st.markdown('<div class="section-header">🔨 &nbsp; CRAFTING REPORT</div>', unsafe_allow_html=True)

if crafted:
    df_c = (pd.DataFrame(list(crafted.items()), columns=["Item","Count"])
            .query("Count > 0")
            .assign(Item=lambda d: d.Item.apply(clean))
            .sort_values("Count", ascending=False).head(15))

    fig = px.bar(df_c, x="Item", y="Count",
                 color="Count", color_continuous_scale=["#2a1e0a","#ffd93d"])
    fig.update_layout(**BASE_LAYOUT,
        title=dict(text="Top Items Crafted", font=dict(color="#ffd93d", size=13)),
        xaxis=dict(gridcolor=GRID_COLOR, tickangle=30),
        yaxis=dict(gridcolor=GRID_COLOR),
        coloraxis_showscale=False, height=360
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════
# AI FEATURES
# ══════════════════════════════════════════════
st.markdown('<div class="section-header">🤖 &nbsp; AI ANALYSIS</div>', unsafe_allow_html=True)

if not api_key:
    st.markdown("""
    <div class="ai-section" style="text-align:center; padding:48px;">
        <div style="font-size:3rem;">🤖</div>
        <div style="font-family:'Press Start 2P',monospace; font-size:0.8rem; color:#7c3aed; margin:12px 0;">AI FEATURES LOCKED</div>
        <div style="font-family:Inter,sans-serif; color:#556; font-size:0.9rem;">
            Add your free Groq API key in the sidebar to unlock<br>
            AI Roast · Session Story · Coach · Death Prediction
        </div>
        <div style="margin-top:16px;">
            <a href="https://console.groq.com" target="_blank" style="color:#7c3aed; font-family:Inter,sans-serif; font-size:0.85rem;">
                → Get your 100% free key at console.groq.com
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    stats_summary = build_stats_summary(stats)

    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Roast Me", "📖 My Story", "🧠 Coach", "🔮 Prediction"])

    with tab1:
        st.markdown('<div class="ai-tab-header">AI ROAST</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Inter,sans-serif; color:#556; font-size:0.85rem; margin-bottom:16px;">A brutally honest, funny roast of your gameplay. Brace yourself.</div>', unsafe_allow_html=True)
        if st.button("🔥 Roast My Gameplay", key="roast"):
            with st.spinner("Summoning the roast demons..."):
                try:
                    result = call_claude(api_key,
                        "You are a savage but funny Minecraft commentator. Roast the player's stats in 6-8 sentences. Be funny, specific, and use the actual numbers. Reference specific stats like salmon kills, death count, jump count etc. End with one backhanded compliment.",
                        f"Roast this Minecraft player based on their stats:\n{stats_summary}"
                    )
                    st.markdown(f'<div class="ai-output">{result}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"API error: {str(e)}")

    with tab2:
        st.markdown('<div class="ai-tab-header">SESSION STORY</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Inter,sans-serif; color:#556; font-size:0.85rem; margin-bottom:16px;">A dramatic narrative of your session, written like an epic adventure.</div>', unsafe_allow_html=True)
        if st.button("📖 Tell My Story", key="story"):
            with st.spinner("Writing your legend..."):
                try:
                    result = call_claude(api_key,
                        "You are a dramatic fantasy narrator. Write a short epic story (8-10 sentences) about this Minecraft player's session. Make it dramatic, use fantasy language, reference specific stats as plot points. The salmon kills must be mentioned heroically. Deaths must be tragic. Jumps must be legendary.",
                        f"Write an epic story about this Minecraft session:\n{stats_summary}"
                    )
                    st.markdown(f'<div class="ai-output">{result}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"API error: {str(e)}")

    with tab3:
        st.markdown('<div class="ai-tab-header">AI COACH</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Inter,sans-serif; color:#556; font-size:0.85rem; margin-bottom:16px;">Real tactical advice for your next session based on your stats.</div>', unsafe_allow_html=True)
        if st.button("🧠 Coach Me", key="coach"):
            with st.spinner("Analysing your gameplay..."):
                try:
                    result = call_claude(api_key,
                        "You are a Minecraft survival expert coach. Analyse the player's stats and give 5 specific, actionable tips for their next session. Reference actual numbers. Mention what they are doing well and what needs improvement. Be direct and practical.",
                        f"Coach this player based on their stats:\n{stats_summary}"
                    )
                    st.markdown(f'<div class="ai-output">{result}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"API error: {str(e)}")

    with tab4:
        st.markdown('<div class="ai-tab-header">DEATH PREDICTION</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Inter,sans-serif; color:#556; font-size:0.85rem; margin-bottom:16px;">Based on your patterns, what will probably kill you next session?</div>', unsafe_allow_html=True)
        if st.button("🔮 Predict My Doom", key="predict"):
            with st.spinner("Consulting the prophecy..."):
                try:
                    result = call_claude(api_key,
                        "You are a dramatic Minecraft oracle. Based on the player's stats, predict what will kill them next session and why. Be specific, use their actual stats as evidence. Give 3 death predictions ranked by probability with reasoning. Be dramatic but accurate.",
                        f"Predict how this player will die next session:\n{stats_summary}"
                    )
                    st.markdown(f'<div class="ai-output">{result}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"API error: {str(e)}")

st.markdown("---")

# FOOTER
st.markdown("""
<div class="footer">
    Built with Python · Pandas · Streamlit · Plotly · Claude AI<br><br>
    <span style="color:#5dff8a;">⛏ Your world. Your data. Your story.</span>
</div>
""", unsafe_allow_html=True)