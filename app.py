# -*- coding: utf-8 -*-
"""Grand Line — Página fan de One Piece hecha con Streamlit."""
import streamlit as st

st.set_page_config(
    page_title="Grand Line | One Piece",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def hat_svg(width: int, uid: str) -> str:
    """Sombrero de paja de Luffy: copa de paja con banda roja (SVG inline)."""
    return f'''<svg width="{width}" viewBox="0 0 120 66" xmlns="http://www.w3.org/2000/svg" style="overflow:visible;vertical-align:middle;">
  <defs>
    <linearGradient id="straw{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fce9a6"/><stop offset="1" stop-color="#e0b04a"/>
    </linearGradient>
    <linearGradient id="brim{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f7d87f"/><stop offset="1" stop-color="#c98f2e"/>
    </linearGradient>
  </defs>
  <ellipse cx="60" cy="50" rx="57" ry="13" fill="url(#brim{uid})" stroke="#8a5a12" stroke-width="2.5"/>
  <path d="M30 50 Q30 10 60 10 Q90 10 90 50 Z" fill="url(#straw{uid})" stroke="#8a5a12" stroke-width="2.5"/>
  <path d="M30 50 Q60 42 90 50 L90 41 Q60 33 30 41 Z" fill="#d0342c" stroke="#8a2019" stroke-width="1.5"/>
  <path d="M38 24 Q60 18 82 24" fill="none" stroke="#c49435" stroke-width="1.5" opacity=".7"/>
  <path d="M34 33 Q60 26 86 33" fill="none" stroke="#c49435" stroke-width="1.5" opacity=".7"/>
</svg>'''

# ============================================================
#  CSS GLOBAL — tema océano nocturno + oro pirata + animaciones
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pirata+One&family=Cinzel:wght@500;700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

/* ---------- base ---------- */
html, body, [class*="css"] { font-family: 'Crimson Text', serif; }
.stApp {
    background:
        radial-gradient(ellipse at 20% -10%, rgba(30,80,140,.35) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 15%, rgba(120,40,140,.18) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 110%, rgba(10,60,110,.45) 0%, transparent 60%),
        linear-gradient(180deg, #050d1a 0%, #071426 45%, #04101f 100%);
}
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 1.2rem; max-width: 1200px;}

/* ---------- animaciones ---------- */
@keyframes float      { 0%,100%{transform:translateY(0) rotate(-4deg);} 50%{transform:translateY(-16px) rotate(4deg);} }
@keyframes bob        { 0%,100%{transform:translateY(0) rotate(-2deg);} 50%{transform:translateY(-8px) rotate(2deg);} }
@keyframes shimmer    { 0%{background-position:-500px 0;} 100%{background-position:500px 0;} }
@keyframes waveMove   { 0%{transform:translateX(0);} 100%{transform:translateX(-50%);} }
@keyframes glowPulse  { 0%,100%{text-shadow:0 0 18px rgba(245,197,66,.55),0 0 60px rgba(245,197,66,.25);} 50%{text-shadow:0 0 34px rgba(245,197,66,.95),0 0 90px rgba(245,197,66,.45);} }
@keyframes fadeUp     { from{opacity:0; transform:translateY(26px);} to{opacity:1; transform:translateY(0);} }
@keyframes sparkle    { 0%,100%{opacity:.25;} 50%{opacity:1;} }
@keyframes spinSlow   { from{transform:rotate(0);} to{transform:rotate(360deg);} }
@keyframes sail       { 0%{transform:translateX(-6vw) translateY(0) rotate(-2deg);} 50%{transform:translateX(46vw) translateY(-10px) rotate(2deg);} 100%{transform:translateX(96vw) translateY(0) rotate(-2deg);} }

/* ---------- héroe ---------- */
.hero {
    position: relative;
    text-align: center;
    padding: 4.2rem 1rem 7.5rem;
    border-radius: 26px;
    overflow: hidden;
    background:
        radial-gradient(ellipse at 50% 0%, rgba(50,110,180,.30) 0%, transparent 60%),
        linear-gradient(180deg, #0a1e38 0%, #0c2b4e 60%, #0e3a66 100%);
    border: 1px solid rgba(245,197,66,.28);
    box-shadow: 0 30px 80px rgba(0,0,0,.55), inset 0 0 120px rgba(10,40,80,.5);
    animation: fadeUp .9s ease both;
}
.hero .stars { position:absolute; inset:0; pointer-events:none; }
.hero .stars span { position:absolute; color:#fdf3c8; font-size:.7rem; animation: sparkle 3s ease-in-out infinite; }
.hero-hat  { font-size: 5.2rem; display:inline-block; animation: float 4.5s ease-in-out infinite; filter: drop-shadow(0 12px 22px rgba(0,0,0,.6)); }
h1.hero-title {
    font-family: 'Pirata One', cursive !important;
    font-size: clamp(3.4rem, 9vw, 6.8rem) !important;
    letter-spacing: .06em !important;
    margin: .2rem 0 0 !important;
    padding: 0 !important;
    color: #f5c542 !important;
    font-weight: 400 !important;
    animation: glowPulse 3.5s ease-in-out infinite;
    line-height: 1.02 !important;
}
.hero-sub {
    font-family:'Cinzel', serif; font-weight:700; letter-spacing:.42em;
    color:#9fc6ef; font-size: clamp(.8rem, 2vw, 1.05rem); margin-top:.4rem; text-transform:uppercase;
}
.hero-quote {
    max-width: 640px; margin: 1.4rem auto 0; font-style: italic;
    color:#d7e6f7; font-size:1.15rem; line-height:1.55; opacity:.92;
}
.hero-quote b { color:#f5c542; font-style:normal; }
.hero-ship { position:absolute; bottom:52px; left:0; font-size:2.6rem; animation: sail 26s linear infinite; filter: drop-shadow(0 6px 10px rgba(0,0,0,.5)); z-index:2; }

/* olas del héroe */
.waves { position:absolute; bottom:-2px; left:0; width:100%; height:110px; overflow:hidden; }
.waves svg { position:absolute; bottom:0; left:0; width:200%; height:100%; animation: waveMove 11s linear infinite; }
.waves.back svg { animation-duration: 19s; opacity:.5; height:120%; }

/* ---------- separador ---------- */
.divider { display:flex; align-items:center; gap:1rem; margin: 2.6rem 0 1.4rem; animation: fadeUp .8s ease both; }
.divider:before,.divider:after { content:""; flex:1; height:1px; background: linear-gradient(90deg, transparent, rgba(245,197,66,.55), transparent); }
.divider .dtitle { font-family:'Pirata One', cursive; font-size:2.3rem; color:#f5c542; letter-spacing:.05em; white-space:nowrap; }
.divider .dsub { display:block; text-align:center; font-family:'Cinzel',serif; font-size:.72rem; letter-spacing:.35em; color:#8fb4dd; }

/* ---------- carteles WANTED ---------- */
.wanted {
    position:relative;
    background:
        radial-gradient(ellipse at 50% 8%, rgba(255,250,225,.9) 0%, rgba(240,222,178,.94) 55%, rgba(214,186,132,.96) 100%);
    border: 3px double #6b4b1e;
    outline: 2px solid rgba(80,55,20,.5);
    outline-offset: -9px;
    border-radius: 6px;
    padding: 1.1rem .8rem 1rem;
    text-align:center;
    color:#3a2409;
    box-shadow: 0 14px 34px rgba(0,0,0,.5), inset 0 0 46px rgba(120,85,35,.28);
    transition: transform .35s cubic-bezier(.2,.9,.3,1.4), box-shadow .35s ease;
    animation: fadeUp .7s ease both;
    height: 100%;
}
.wanted:hover {
    transform: translateY(-10px) rotate(-1.3deg) scale(1.03);
    box-shadow: 0 26px 54px rgba(0,0,0,.65), 0 0 34px rgba(245,197,66,.35), inset 0 0 46px rgba(120,85,35,.28);
}
.wanted .wtop { font-family:'Cinzel',serif; font-weight:900; font-size:1.55rem; letter-spacing:.16em; border-bottom:2px solid rgba(80,55,20,.55); padding-bottom:.15rem; }
.wanted .wface { font-size:3.4rem; margin:.45rem 0 .2rem; display:inline-block; transition: transform .4s ease; }
.wanted:hover .wface { transform: scale(1.22) rotate(6deg); }
.wanted .wdead { font-family:'Cinzel',serif; font-size:.62rem; font-weight:700; letter-spacing:.3em; opacity:.85; }
.wanted .wname { font-family:'Pirata One', cursive; font-size:1.5rem; margin:.15rem 0 0; color:#4a2c08; line-height:1.05; }
.wanted .wrole { font-size:.85rem; font-style:italic; opacity:.85; min-height:2.1em; line-height:1.15; }
.wanted .wbounty { font-family:'Cinzel',serif; font-weight:900; font-size:1.02rem; margin-top:.35rem; color:#5a3408; letter-spacing:.02em; }
.wanted .wbounty small { display:block; font-size:.58rem; letter-spacing:.28em; font-weight:700; opacity:.75; }
.wanted .wfruit { margin-top:.4rem; font-size:.78rem; background:rgba(90,60,20,.14); border:1px solid rgba(90,60,20,.3); border-radius:20px; display:inline-block; padding:.12rem .6rem; }

/* ---------- tarjetas genéricas ---------- */
.card {
    background: linear-gradient(160deg, rgba(16,38,66,.92) 0%, rgba(9,24,44,.96) 100%);
    border: 1px solid rgba(120,170,230,.22);
    border-radius: 18px;
    padding: 1.3rem 1.25rem 1.15rem;
    height: 100%;
    box-shadow: 0 12px 30px rgba(0,0,0,.45);
    transition: transform .3s ease, border-color .3s ease, box-shadow .3s ease;
    animation: fadeUp .7s ease both;
    position: relative;
    overflow: hidden;
}
.card:hover { transform: translateY(-7px); border-color: rgba(245,197,66,.6); box-shadow: 0 22px 46px rgba(0,0,0,.6), 0 0 26px rgba(245,197,66,.18); }
.card .cicon { font-size:2.6rem; display:inline-block; animation: bob 3.6s ease-in-out infinite; }
.card h4 { font-family:'Pirata One', cursive !important; font-size:1.55rem !important; color:#f5c542 !important; margin:.35rem 0 .25rem !important; padding:0 !important; letter-spacing:.03em !important; font-weight:400 !important; }
.card .ctag { font-family:'Cinzel',serif; font-size:.62rem; letter-spacing:.3em; color:#8fb4dd; text-transform:uppercase; }
.card p { color:#c9d8ea; font-size:.98rem; line-height:1.5; margin:.4rem 0 0; }
.card .cband { position:absolute; top:0; left:0; width:100%; height:4px; background:linear-gradient(90deg,#f5c542,#e07b39,#f5c542); background-size:200% 100%; animation: shimmer 4s linear infinite; }

/* ---------- línea de tiempo ---------- */
.timeline { position:relative; margin:.5rem 0 0 .4rem; padding-left:1.9rem; }
.timeline:before { content:""; position:absolute; left:9px; top:6px; bottom:6px; width:3px; border-radius:3px;
    background: linear-gradient(180deg,#f5c542 0%,#e07b39 50%,#3aa0d8 100%); box-shadow:0 0 14px rgba(245,197,66,.5); }
.tl-item { position:relative; padding: .1rem 0 1.5rem; animation: fadeUp .7s ease both; }
.tl-item:before { content:""; position:absolute; left:-1.62rem; top:.42rem; width:13px; height:13px; border-radius:50%;
    background:#f5c542; border:3px solid #0a1628; box-shadow:0 0 12px rgba(245,197,66,.8); }
.tl-item h5 { font-family:'Pirata One',cursive !important; font-size:1.35rem !important; color:#ffd968 !important; margin:0 !important; padding:0 !important; font-weight:400 !important; }
.tl-item .tlmeta { font-family:'Cinzel',serif; font-size:.62rem; letter-spacing:.26em; color:#7fa8d4; text-transform:uppercase; }
.tl-item p { color:#c3d4e8; margin:.25rem 0 0; font-size:.97rem; line-height:1.5; }

/* ---------- barras de recompensa ---------- */
.bounty-row { margin-bottom: .95rem; animation: fadeUp .7s ease both; }
.bounty-row .blabel { display:flex; justify-content:space-between; font-family:'Cinzel',serif; font-size:.8rem; letter-spacing:.06em; color:#dce8f5; margin-bottom:.28rem; }
.bounty-row .blabel b { color:#f5c542; }
.bounty-track { height: 14px; background: rgba(255,255,255,.07); border-radius: 10px; overflow:hidden; border:1px solid rgba(255,255,255,.1); }
.bounty-fill { height:100%; border-radius:10px;
    background: linear-gradient(90deg,#8a5a12,#f5c542 55%,#fff3c4 80%,#f5c542);
    background-size: 300% 100%; animation: shimmer 3.2s linear infinite;
    box-shadow: 0 0 14px rgba(245,197,66,.6); }

/* ---------- píldoras / badges ---------- */
.pill { display:inline-block; font-family:'Cinzel',serif; font-size:.66rem; font-weight:700; letter-spacing:.18em;
    padding:.28rem .8rem; border-radius:30px; margin:.15rem .2rem; text-transform:uppercase;
    border:1px solid rgba(245,197,66,.5); color:#ffd968; background:rgba(245,197,66,.08); }

/* ---------- log pose (brújula) ---------- */
.logpose { display:inline-block; animation: spinSlow 14s linear infinite; font-size:2rem; }

/* ---------- pestañas Streamlit ---------- */
div[role="tablist"] { gap:.45rem !important; justify-content:center !important; border-bottom:none !important; flex-wrap:wrap; }
div[role="tablist"]:after, div[role="tablist"]:before { display:none !important; }
[data-testid="stTab"] {
    font-family:'Cinzel',serif !important; font-weight:700 !important; letter-spacing:.08em !important;
    background: rgba(16,38,66,.65) !important; border:1px solid rgba(120,170,230,.25) !important;
    border-radius: 30px !important; padding: .55rem 1.25rem !important; color:#bcd3ea !important;
    transition: all .25s ease !important;
}
[data-testid="stTab"] p { font-family:'Cinzel',serif !important; font-weight:700 !important; color:inherit !important; }
[data-testid="stTab"]:hover { border-color:#f5c542 !important; color:#ffd968 !important; transform: translateY(-2px); }
[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(245,197,66,.22), rgba(224,123,57,.18)) !important;
    border-color:#f5c542 !important; color:#ffd968 !important;
    box-shadow: 0 0 18px rgba(245,197,66,.28);
}
[data-testid="stTab"] [data-testid="stMarkdownContainer"] ~ div { display:none !important; }

/* ---------- botones ---------- */
.stButton > button {
    font-family:'Cinzel',serif !important; font-weight:700; letter-spacing:.12em;
    background: linear-gradient(135deg,#f5c542,#e07b39) !important; color:#1c1002 !important;
    border:none !important; border-radius: 30px !important; padding:.6rem 1.6rem !important;
    box-shadow: 0 8px 22px rgba(224,123,57,.4); transition: all .25s ease !important;
}
.stButton > button:hover { transform: translateY(-3px) scale(1.03); box-shadow: 0 14px 30px rgba(245,197,66,.5); }

/* ---------- historia del anime ---------- */
@keyframes flowY { 0%{background-position:0 0;} 100%{background-position:0 300%;} }
@keyframes popIn { 0%{opacity:0; transform:scale(.7);} 70%{transform:scale(1.08);} 100%{opacity:1; transform:scale(1);} }
.anime-stats { display:flex; gap:1rem; justify-content:center; flex-wrap:wrap; margin:.6rem 0 1.8rem; }
.astat { flex:1; min-width:150px; max-width:230px; text-align:center; padding:1.05rem .8rem .95rem; border-radius:16px;
    background: linear-gradient(160deg, rgba(22,48,84,.92), rgba(10,25,48,.96));
    border:1px solid rgba(245,197,66,.35); box-shadow:0 10px 26px rgba(0,0,0,.45);
    transition: transform .3s ease, box-shadow .3s ease; animation: fadeUp .7s ease both; position:relative; overflow:hidden; }
.astat:before { content:""; position:absolute; top:0; left:0; width:100%; height:3px;
    background:linear-gradient(90deg,#f5c542,#e07b39,#f5c542); background-size:200% 100%; animation: shimmer 4s linear infinite; }
.astat:hover { transform: translateY(-7px) scale(1.05); box-shadow:0 18px 40px rgba(0,0,0,.6), 0 0 26px rgba(245,197,66,.32); }
.astat .semoji { font-size:1.5rem; display:block; margin-bottom:.15rem; }
.astat .snum { font-family:'Pirata One',cursive; font-size:2.35rem; color:#f5c542; animation: glowPulse 3.5s ease-in-out infinite; line-height:1.05; }
.astat .slab { font-family:'Cinzel',serif; font-size:.6rem; letter-spacing:.22em; color:#9fc6ef; margin-top:.4rem; text-transform:uppercase; }

.atl { position:relative; margin-top:1.6rem; padding-bottom:.5rem; }
.atl:before { content:""; position:absolute; left:50%; top:8px; bottom:8px; width:4px; transform:translateX(-50%); border-radius:4px;
    background: linear-gradient(180deg,#f5c542,#e07b39,#3aa0d8,#f5c542); background-size:100% 300%;
    animation: flowY 9s linear infinite; box-shadow:0 0 18px rgba(245,197,66,.55); }
.atl-row { display:grid; grid-template-columns:1fr 96px 1fr; align-items:center; margin-bottom:1.15rem; }
.atl-year { width:66px; height:66px; margin:0 auto; border-radius:50%; display:flex; align-items:center; justify-content:center;
    font-family:'Pirata One',cursive; font-size:1.2rem; color:#241503;
    background: radial-gradient(circle at 35% 30%, #ffe9a8, #f5c542 55%, #c98f1e);
    border:3px solid #8a5a12; box-shadow:0 0 24px rgba(245,197,66,.65); z-index:1;
    transition: transform .3s ease; animation: popIn .6s ease both; }
.atl-row:hover .atl-year { transform: scale(1.18) rotate(-8deg); }
.atl-card { background: linear-gradient(160deg, rgba(16,38,66,.92), rgba(9,24,44,.96)); border:1px solid rgba(120,170,230,.25);
    border-radius:16px; padding:.95rem 1.15rem .9rem; box-shadow:0 10px 26px rgba(0,0,0,.45);
    transition: all .3s ease; animation: fadeUp .7s ease both; }
.atl-card:hover { border-color:rgba(245,197,66,.65); transform:translateY(-5px);
    box-shadow:0 18px 40px rgba(0,0,0,.6), 0 0 26px rgba(245,197,66,.22); }
.atl-card .aicon { float:right; font-size:1.7rem; margin-left:.6rem; }
.atl-card h6 { font-family:'Pirata One',cursive !important; font-size:1.3rem !important; color:#ffd968 !important;
    margin:0 0 .25rem !important; padding:0 !important; font-weight:400 !important; }
.atl-card p { color:#c3d4e8; margin:0; font-size:.93rem; line-height:1.45; }

/* ---------- footer ---------- */
.footer { position:relative; margin-top:3.5rem; text-align:center; padding:2.6rem 1rem 2rem; border-radius:22px; overflow:hidden;
    background: linear-gradient(180deg, rgba(10,30,56,.8), rgba(6,16,32,.95)); border:1px solid rgba(120,170,230,.18); }
.footer .fquote { font-family:'Pirata One',cursive; font-size:1.9rem; color:#f5c542; }
.footer .fsub { color:#9db8d8; font-style:italic; margin-top:.4rem; }
.footer .fnote { margin-top:1.1rem; font-size:.75rem; color:#5f7fa2; letter-spacing:.08em; }
</style>
""", unsafe_allow_html=True)

# ============================================================
#  HÉROE
# ============================================================
st.markdown(f"""
<div class="hero">
  <div class="stars">
    <span style="top:12%;left:8%;">✦</span><span style="top:22%;left:18%;animation-delay:.7s;">✧</span>
    <span style="top:9%;left:38%;animation-delay:1.4s;">✦</span><span style="top:18%;left:62%;animation-delay:.3s;">✧</span>
    <span style="top:8%;left:80%;animation-delay:1s;">✦</span><span style="top:30%;left:90%;animation-delay:1.8s;">✧</span>
    <span style="top:34%;left:4%;animation-delay:2.2s;">✦</span><span style="top:40%;left:72%;animation-delay:.9s;">✦</span>
  </div>
  <div class="hero-hat">{hat_svg(128, "h")}</div>
  <h1 class="hero-title">GRAND LINE</h1>
  <div class="hero-sub">· Un homenaje a One Piece ·</div>
  <p class="hero-quote">«¿Mi tesoro? Si lo queréis, es vuestro… ¡Buscadlo! ¡Lo dejé todo en <b>ese lugar</b>!»<br>
  — Gol D. Roger, el Rey de los Piratas</p>
  <div class="hero-ship">⛵</div>
  <div class="waves back">
    <svg viewBox="0 0 1200 110" preserveAspectRatio="none">
      <path d="M0,55 C150,95 300,15 450,55 C600,95 750,15 900,55 C1050,95 1200,15 1350,55 C1500,95 1650,15 1800,55 C1950,95 2100,15 2250,55 L2400,55 L2400,110 L0,110 Z" fill="#0d3358"/>
    </svg>
  </div>
  <div class="waves">
    <svg viewBox="0 0 1200 110" preserveAspectRatio="none">
      <path d="M0,65 C160,105 320,25 480,65 C640,105 800,25 960,65 C1120,105 1280,25 1440,65 C1600,105 1760,25 1920,65 C2080,105 2240,25 2400,65 L2400,110 L0,110 Z" fill="#0a2440"/>
    </svg>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:1.2rem;">
  <span class="pill">🏴‍☠️ Piratas del Sombrero de Paja</span>
  <span class="pill">🍈 Frutas del Diablo</span>
  <span class="pill">🗺️ 11 Sagas</span>
  <span class="pill">👑 En busca del One Piece</span>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  PESTAÑAS
# ============================================================
tab_crew, tab_fruits, tab_sagas, tab_anime, tab_bounty, tab_quiz = st.tabs([
    "🏴‍☠️ La Tripulación", "🍈 Frutas del Diablo", "🗺️ Las Sagas", "📺 Historia del Anime", "💰 Recompensas", "🧭 Pon a prueba tu Haki"
])

# ------------------------------------------------------------
#  TRIPULACIÓN — carteles de SE BUSCA
# ------------------------------------------------------------
CREW = [
    (hat_svg(64, "l"), "Monkey D. Luffy", "Capitán · Futuro Rey de los Piratas", "3.000.000.000", "Gomu Gomu no Mi (Nika)"),
    ("⚔️", "Roronoa Zoro", "Espadachín · Estilo de tres espadas", "1.111.000.000", "—"),
    ("🍊", "Nami", "Navegante · Ladrona de mapas", "366.000.000", "—"),
    ("🎯", "Usopp", "Tirador · 'Dios' Usopp", "500.000.000", "—"),
    ("🍳", "Sanji", "Cocinero · Pierna Negra", "1.032.000.000", "—"),
    ("🦌", "Tony Tony Chopper", "Médico · Renito mascota(?)", "1.000", "Hito Hito no Mi"),
    ("🌸", "Nico Robin", "Arqueóloga · Niña demonio", "930.000.000", "Hana Hana no Mi"),
    ("🤖", "Franky", "Carpintero · ¡SUPER! Cyborg", "394.000.000", "—"),
    ("🎻", "Brook", "Músico · Rey del Soul", "383.000.000", "Yomi Yomi no Mi"),
    ("🐳", "Jinbe", "Timonel · Caballero del Mar", "1.100.000.000", "—"),
]

with tab_crew:
    st.markdown("""
    <div class="divider"><div><span class="dtitle">Los Sombrero de Paja</span>
    <span class="dsub">Mugiwara no Ichimi</span></div></div>
    """, unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:#a9c2dd;font-style:italic;margin-top:-0.4rem;'>"
        "Diez sueños, un solo barco. Pasa el cursor sobre cada cartel… si te atreves. 🏴‍☠️</p>",
        unsafe_allow_html=True,
    )
    for row_start in range(0, len(CREW), 5):
        cols = st.columns(5, gap="small")
        for col, (face, name, role, bounty, fruit) in zip(cols, CREW[row_start:row_start + 5]):
            fruit_html = f'<div class="wfruit">🍈 {fruit}</div>' if fruit != "—" else '<div class="wfruit" style="opacity:.55;">Sin fruta</div>'
            col.markdown(f"""
            <div class="wanted">
              <div class="wtop">WANTED</div>
              <div class="wface">{face}</div>
              <div class="wdead">DEAD OR ALIVE</div>
              <div class="wname">{name}</div>
              <div class="wrole">{role}</div>
              <div class="wbounty"><small>RECOMPENSA</small>฿ {bounty}</div>
              {fruit_html}
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
#  FRUTAS DEL DIABLO
# ------------------------------------------------------------
with tab_fruits:
    st.markdown("""
    <div class="divider"><div><span class="dtitle">Frutas del Diablo</span>
    <span class="dsub">Akuma no Mi · El poder del mar tiene un precio</span></div></div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    c1.markdown("""
    <div class="card"><div class="cband"></div>
      <span class="cicon">✨</span>
      <div class="ctag">Tipo I</div><h4>Paramecia</h4>
      <p>Otorgan poderes sobrehumanos que alteran el cuerpo o el entorno: cuerpos de goma,
      ondas de choque, creación de hilos… Las más comunes y las más impredecibles.</p>
      <p style="color:#8fb4dd;font-size:.85rem;">Ej.: Gomu Gomu, Ope Ope, Hana Hana</p>
    </div>""", unsafe_allow_html=True)
    c2.markdown("""
    <div class="card"><div class="cband"></div>
      <span class="cicon">🐉</span>
      <div class="ctag">Tipo II</div><h4>Zoan</h4>
      <p>Permiten transformarse en un animal o en híbrido. Las Zoan Míticas —fénix, dragones,
      dioses— son incluso más raras que las Logia y esconden voluntades propias.</p>
      <p style="color:#8fb4dd;font-size:.85rem;">Ej.: Hito Hito (Nika), Uo Uo, Tori Tori (Fénix)</p>
    </div>""", unsafe_allow_html=True)
    c3.markdown("""
    <div class="card"><div class="cband"></div>
      <span class="cicon">🔥</span>
      <div class="ctag">Tipo III</div><h4>Logia</h4>
      <p>Convierten al usuario en un elemento natural: fuego, hielo, luz, oscuridad…
      Intangibles ante ataques normales, solo el Haki puede alcanzarlos.</p>
      <p style="color:#8fb4dd;font-size:.85rem;">Ej.: Mera Mera, Pika Pika, Yami Yami</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card" style="text-align:center;">
      <span style="font-size:2rem;">🌊</span>
      <h4 style="margin-top:.2rem;">La maldición del mar</h4>
      <p style="max-width:720px;margin:.4rem auto 0;">Quien muerde una Fruta del Diablo obtiene un poder extraordinario…
      pero el océano lo rechaza para siempre: los usuarios se hunden como martillos en el agua
      y el <b style="color:#ffd968;">kairoseki</b> (piedra marina) anula por completo sus habilidades.
      Un precio cruel para quienes viven persiguiendo el mar más grande del mundo.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
#  SAGAS — línea de tiempo
# ------------------------------------------------------------
SAGAS = [
    ("East Blue", "El comienzo · Cap. 1", "Un chico de goma con un sombrero de paja recluta a un espadachín, una ladrona, un mentiroso y un cocinero. Nace la leyenda."),
    ("Alabasta", "El reino de arena", "La tripulación cruza la Grand Line para salvar un reino de la guerra civil orquestada por Crocodile y Baroque Works."),
    ("Skypiea", "La isla del cielo", "Una isla en el cielo, un 'dios' con poder del rayo y una campana que suena tras 400 años. El romance de la aventura en estado puro."),
    ("Water 7 / Enies Lobby", "La declaración de guerra", "«¡Quiero vivir!» — Robin. Los Sombrero de Paja le declaran la guerra al Gobierno Mundial y queman su bandera."),
    ("Thriller Bark", "La isla fantasma", "Sombras robadas, un esqueleto caballeroso y la promesa de reencontrarse con una ballena en Cabo Gemelos."),
    ("Guerra de Marineford", "La cima de la guerra", "La guerra que cambió el mundo. La era de Barbablanca termina y Luffy pierde lo que más quería proteger."),
    ("Isla Gyojin", "Dos años después", "La tripulación se reúne más fuerte que nunca y desciende 10.000 metros bajo el mar hacia el Nuevo Mundo."),
    ("Dressrosa", "El coliseo de juguetes", "Un país de cuentos con un rey de hilos. La alianza pirata derriba a un Shichibukai y nace la Gran Flota."),
    ("Whole Cake Island", "El rescate de Sanji", "Té, bodas falsas y una Emperatriz del Mar. Luffy contra Katakuri: el duelo que despertó su Haki de Observación."),
    ("Wano", "El país de los samuráis", "Veinte años de espera, nueve fundas rojas y el despertar de Nika. Luffy se convierte en Emperador del Mar."),
    ("Egghead", "La isla del futuro", "El laboratorio del Dr. Vegapunk, secretos del Siglo Vacío y el inicio de la guerra final. El One Piece está cerca."),
]

with tab_sagas:
    st.markdown("""
    <div class="divider"><div><span class="dtitle">La Gran Travesía</span>
    <span class="dsub">De East Blue a la última isla</span></div></div>
    """, unsafe_allow_html=True)
    left, right = st.columns([3, 2], gap="large")
    with left:
        items = "".join(
            f"""<div class="tl-item" style="animation-delay:{i * .08:.2f}s;">
                 <div class="tlmeta">{meta}</div><h5>{i+1}. {name}</h5><p>{desc}</p></div>"""
            for i, (name, meta, desc) in enumerate(SAGAS)
        )
        st.markdown(f'<div class="timeline">{items}</div>', unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="card" style="text-align:center;">
          <span class="logpose">🧭</span>
          <h4>Log Pose</h4>
          <p>En la Grand Line las brújulas normales enloquecen. Solo un Log Pose puede guiarte
          de isla en isla… y solo el <b style="color:#ffd968;">Road Poneglyph</b> ×4 revela Laugh Tale.</p>
        </div>
        <div style="height:1rem;"></div>
        <div class="card">
          <h4 style="text-align:center;">📜 Cifras de leyenda</h4>
          <p style="text-align:center;">
            <b style="color:#ffd968;font-size:1.6rem;">1.100+</b> capítulos del manga<br>
            <b style="color:#ffd968;font-size:1.6rem;">1.100+</b> episodios del anime<br>
            <b style="color:#ffd968;font-size:1.6rem;">500M+</b> copias vendidas<br>
            <span style="font-size:.85rem;color:#8fb4dd;">El manga más vendido de la historia ✒️ Eiichiro Oda, desde 1997</span>
          </p>
        </div>
        <div style="height:1rem;"></div>
        <div class="card" style="text-align:center;">
          <span class="cicon">🔔</span>
          <h4>¿Sabías que…?</h4>
          <p>Oda prometió que el final de One Piece haría que la Guerra de Marineford
          «pareciera un juego de niños». El viaje final ya ha comenzado.</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------
#  HISTORIA DEL ANIME — línea de tiempo central animada
# ------------------------------------------------------------
ANIME_HITOS = [
    ("1997", "✒️", "Nace el manga", "Eiichiro Oda publica el capítulo 1, «Romance Dawn», en la Weekly Shōnen Jump. Nadie imaginaba que sería el manga más vendido de la historia."),
    ("1999", "📺", "¡Zarpa el anime!", "El 20 de octubre, Toei Animation estrena One Piece en Fuji TV. El opening «We Are!» de Hiroshi Kitadani se convierte en himno de toda una generación."),
    ("2000", "🎬", "Primera película", "One Piece llega a los cines japoneses. Sería la primera de más de 15 películas de la franquicia."),
    ("2011", "⏳", "El salto temporal", "Tras la Guerra de Marineford, el anime da el salto de 2 años: nuevos diseños, nuevos poderes y el reencuentro más esperado en la Isla Gyojin."),
    ("2019", "🎆", "20.º aniversario", "Se estrena One Piece: Stampede y arranca el arco de Wano, con una dirección de arte que revoluciona por completo el estilo visual del anime."),
    ("2021", "💯", "Episodio 1000", "«¡Soy Monkey D. Luffy! ¡El hombre que se convertirá en el Rey de los Piratas!». El episodio 1000 se celebra con eventos en todo el mundo."),
    ("2022", "🎤", "Film: Red", "La película de Uta arrasa en taquilla y se convierte en la más exitosa de la saga. Sus canciones dominan las listas musicales de Japón."),
    ("2023", "🔥", "Gear 5 y Netflix", "El episodio 1071 anima el despertar de Nika y colapsa las plataformas de streaming. Meses después, el live-action de Netflix es n.º 1 en más de 80 países."),
    ("2025", "🌅", "THE ONE PIECE", "WIT Studio (Attack on Titan) prepara el remake del anime desde East Blue, mientras la serie original navega rumbo a su saga final."),
]

with tab_anime:
    st.markdown("""
    <div class="divider"><div><span class="dtitle">Historia del Anime</span>
    <span class="dsub">Más de 25 años navegando en la televisión</span></div></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="anime-stats">
      <div class="astat" style="animation-delay:.05s;"><span class="semoji">📺</span><div class="snum">1999</div><div class="slab">Año de estreno</div></div>
      <div class="astat" style="animation-delay:.15s;"><span class="semoji">🎞️</span><div class="snum">1.100+</div><div class="slab">Episodios emitidos</div></div>
      <div class="astat" style="animation-delay:.25s;"><span class="semoji">🎬</span><div class="snum">15</div><div class="slab">Películas en cines</div></div>
      <div class="astat" style="animation-delay:.35s;"><span class="semoji">🎵</span><div class="snum">26</div><div class="slab">Openings icónicos</div></div>
    </div>
    """, unsafe_allow_html=True)

    rows = []
    for i, (year, icon, title, desc) in enumerate(ANIME_HITOS):
        card = (f'<div class="atl-card" style="animation-delay:{i * .09:.2f}s;">'
                f'<span class="aicon">{icon}</span><h6>{title}</h6><p>{desc}</p></div>')
        year_badge = f'<div class="atl-year" style="animation-delay:{i * .09:.2f}s;">{year}</div>'
        if i % 2 == 0:
            rows.append(f'<div class="atl-row"><div>{card}</div><div>{year_badge}</div><div></div></div>')
        else:
            rows.append(f'<div class="atl-row"><div></div><div>{year_badge}</div><div>{card}</div></div>')
    st.markdown(f'<div class="atl">{"".join(rows)}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align:center;margin-top:1.2rem;">
      <span class="cicon">🎶</span>
      <h4>«¡Arittake no yume o kakiatsume!»</h4>
      <p style="max-width:700px;margin:.4rem auto 0;">Del «We Are!» original al «UUUUUS!» de la saga final,
      cada opening marca una era. Millones de fans no pueden escuchar los primeros acordes
      de <b style="color:#ffd968;">We Are!</b> sin que se les ponga la piel de gallina. ¡Esa es la magia de One Piece!</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
#  RECOMPENSAS — barras animadas
# ------------------------------------------------------------
BOUNTIES = [
    ("Gol D. Roger 👑", 5_564_800_000),
    ("Edward Newgate 'Barbablanca' 🌊", 5_046_000_000),
    ("Kaido de las Bestias 🐉", 4_611_100_000),
    ("Big Mom 🍰", 4_388_000_000),
    ("Shanks el Pelirrojo 🍶", 4_048_900_000),
    ("Barbanegra ⚫", 3_996_000_000),
    ("Monkey D. Luffy ☀️", 3_000_000_000),
    ("Trafalgar Law 🩺", 3_000_000_000),
    ("Eustass Kid ⚙️", 3_000_000_000),
]

with tab_bounty:
    st.markdown("""
    <div class="divider"><div><span class="dtitle">Las Mayores Recompensas</span>
    <span class="dsub">Los monstruos que gobiernan los mares</span></div></div>
    """, unsafe_allow_html=True)
    max_b = BOUNTIES[0][1]
    rows = "".join(
        f"""<div class="bounty-row" style="animation-delay:{i * .1:.2f}s;">
              <div class="blabel"><span>{name}</span><b>฿ {val:,}</b></div>
              <div class="bounty-track"><div class="bounty-fill" style="width:{val / max_b * 100:.1f}%;"></div></div>
            </div>"""
        for i, (name, val) in enumerate(BOUNTIES)
    )
    st.markdown(f'<div class="card"><div class="cband"></div>{rows}'
                '<p style="text-align:center;font-size:.8rem;color:#7fa0c4;margin-top:1rem;">'
                '฿ = Berries · Recompensas conocidas hasta la saga de Egghead</p></div>',
                unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;font-family:Cinzel,serif;color:#9fc6ef;letter-spacing:.2em;'>⚖️ ¿CUÁNTO VALDRÍA TU CABEZA?</h4>", unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns([1, 2, 1])
    with sc2:
        danger = st.slider("Nivel de amenaza al Gobierno Mundial", 0, 100, 42, label_visibility="collapsed")
        my_bounty = int((danger / 100) ** 2.2 * 5_600_000_000)
        if danger < 15:
            rank, icon = "Grumete de East Blue", "🐣"
        elif danger < 40:
            rank, icon = "Novato de la Grand Line", "⛵"
        elif danger < 65:
            rank, icon = "Supernova de la Peor Generación", "💥"
        elif danger < 85:
            rank, icon = "Comandante Yonko", "⚡"
        else:
            rank, icon = "¡EMPERADOR DEL MAR!", "👑"
        st.markdown(f"""
        <div class="wanted" style="max-width:340px;margin:0 auto;">
          <div class="wtop">WANTED</div>
          <div class="wface">{icon}</div>
          <div class="wdead">DEAD OR ALIVE</div>
          <div class="wname">Tú, nakama</div>
          <div class="wrole">{rank}</div>
          <div class="wbounty"><small>RECOMPENSA</small>฿ {my_bounty:,}</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------
#  QUIZ
# ------------------------------------------------------------
QUIZ = [
    ("¿Cuál es el verdadero nombre de la fruta de Luffy?", ["Gomu Gomu no Mi", "Hito Hito no Mi: modelo Nika", "Nika Nika no Mi", "Sun Sun no Mi"], 1),
    ("¿Cuántas espadas usa Zoro en su estilo característico?", ["Una", "Dos", "Tres", "Cuatro"], 2),
    ("¿Quién fue el primer barco… digo, primer miembro en unirse a Luffy?", ["Nami", "Usopp", "Sanji", "Zoro"], 3),
    ("¿Cómo se llama la isla final donde espera el One Piece?", ["Raftel", "Laugh Tale", "Elbaf", "Mary Geoise"], 1),
    ("¿Qué promesa une a Shanks y Luffy?", ["Repartirse el tesoro", "Devolverle el sombrero de paja al convertirse en un gran pirata", "Hundir la Marina", "Encontrar a Roger"], 1),
]

with tab_quiz:
    st.markdown("""
    <div class="divider"><div><span class="dtitle">Pon a prueba tu Haki</span>
    <span class="dsub">5 preguntas · Solo un verdadero nakama las supera</span></div></div>
    """, unsafe_allow_html=True)
    qc1, qc2, qc3 = st.columns([1, 2, 1])
    with qc2:
        answers = []
        for i, (q, opts, _) in enumerate(QUIZ):
            st.markdown(f"<p style='font-family:Cinzel,serif;color:#ffd968;font-weight:700;margin-bottom:.2rem;'>{i+1}. {q}</p>", unsafe_allow_html=True)
            answers.append(st.radio(q, opts, index=None, key=f"q{i}", label_visibility="collapsed"))
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        if st.button("⚓ ¡Zarpar con mis respuestas!", use_container_width=True):
            score = sum(1 for (q, opts, correct), a in zip(QUIZ, answers) if a == opts[correct])
            if score == 5:
                title, icon, msg = "¡REY DE LOS PIRATAS!", "👑", "Gol D. Roger estaría orgulloso. El One Piece es prácticamente tuyo."
                st.balloons()
            elif score >= 4:
                title, icon, msg = "Yonko en ascenso", "⚡", "Los periódicos del mundo ya hablan de ti, Emperador."
                st.balloons()
            elif score >= 3:
                title, icon, msg = "Supernova prometedor", "💥", "La Peor Generación te espera. ¡Sigue navegando!"
            elif score >= 1:
                title, icon, msg = "Grumete con futuro", "⛵", "Todo pirata legendario empezó en un bote de remos."
            else:
                title, icon, msg = "¿Marine infiltrado?", "🚨", "Ni Buggy lo haría peor… ¡pero Buggy llegó a Emperador!"
            st.markdown(f"""
            <div class="card" style="text-align:center;border-color:rgba(245,197,66,.6);">
              <span style="font-size:3rem;">{icon}</span>
              <h4 style="font-size:2rem;">{title}</h4>
              <p style="font-family:Cinzel,serif;letter-spacing:.2em;color:#ffd968;font-size:1.1rem;">{score} / 5 ACIERTOS</p>
              <p>{msg}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
#  FOOTER
# ============================================================
st.markdown("""
<div class="footer">
  <div style="font-size:2.2rem;margin-bottom:.4rem;">🏴‍☠️</div>
  <div class="fquote">«El One Piece… ¡existe!»</div>
  <div class="fsub">— Edward Newgate, Barbablanca. Sus últimas palabras encendieron la Gran Era Pirata.</div>
  <div class="fnote">Página fan sin ánimo de lucro · One Piece © Eiichiro Oda / Shueisha · Hecha con ❤️ y Streamlit</div>
</div>
""", unsafe_allow_html=True)
