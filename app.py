import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse 
import time 

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Cycle Vibe Check ✨", # Magical Title
    page_icon="💖",
    layout="wide", 
)

# ---------- CUSTOM CSS (Soft, Readable, Compact) ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;800;900&display=swap'); /* Cute modern font (Nunito) */
    :root {
        --ink: #2c1124;
        --muted: #6a3a60;
        --accent: #ff4f8a;
        --accent-soft: #ff7fb1;
        --panel: #fff1f6;
        --panel-2: #f7e8ff;
        --line: #efc7dd;
        --glow: #ff6fa5;
    }
    /* Hide fullscreen expand icons to keep everything inline */
    button[title="View fullscreen"] { display: none !important; }
    .stApp {
        background: radial-gradient(circle at 18% 8%, #ffe1f1 0%, #ffd7eb 28%, #f3daff 65%, #f5eefe 100%);
        color: var(--ink);
        font-family: 'Nunito', sans-serif; 
    }
    .block-container {
        padding-top: 0.6rem;
        padding-bottom: 0.6rem;
        max-width: 1200px;
    }
    .main-block {
        background: linear-gradient(135deg, rgba(255, 241, 246, 0.96), rgba(247, 232, 255, 0.96));
        border-radius: 24px;
        padding: 1.1rem 1.25rem; 
        box-shadow: 0 14px 30px rgba(117, 26, 86, 0.12), 0 0 16px rgba(255, 150, 210, 0.35);
        border: 1px solid rgba(239, 199, 221, 0.7); 
        margin: 0 auto;
    }
    /* --- HEADER AND TITLE --- */
    .header-gradient {
        background: linear-gradient(90deg, #ff7fb8, #f3b4ff);
        border-radius: 18px;
        padding: 0.4rem 0.7rem;
        margin: -0.2rem -0.2rem 0.85rem -0.2rem;
        box-shadow: inset 0 -3px 8px rgba(255, 255, 255, 0.65);
    }
    .title-text {
        font-size: 2.0rem;
        font-weight: 900;
        letter-spacing: -0.05em;
        color: var(--ink);
        text-shadow: 1px 1px 4px rgba(255, 255, 255, 0.85);
        text-align: center;
    }
    .subtitle-text {
        font-size: 0.92rem;
        opacity: 0.9;
        color: var(--muted);
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.35rem;
    }
    /* Status Badge under the title */
    .header-status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.3rem 0.8rem;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 800;
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(255, 125, 185, 0.4);
        color: var(--ink);
        box-shadow: 0 0 12px rgba(255, 120, 190, 0.3);
    }
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #ff99d4, transparent);
        margin: 0.7rem 0; 
        opacity: 0.5;
    }
    h3 {
        margin-bottom: 0.45rem;
        margin-top: 0.1rem;
        color: var(--ink);
    }
    .section-label {
        font-size: 0.85rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: var(--muted);
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .field-label-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.35rem;
        font-weight: 800;
        color: var(--ink);
        margin-bottom: 0.3rem;
        font-size: 0.95rem;
    }
    .help-dot {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff7fb8, #ff5f9e);
        color: white;
        font-weight: 900;
        font-size: 0.75rem;
        cursor: help;
        position: relative;
        flex-shrink: 0;
    }
    .help-dot::after {
        content: attr(data-tip);
        position: absolute;
        left: 50%;
        bottom: 135%;
        transform: translateX(-50%);
        background: rgba(44, 17, 36, 0.95);
        color: #fff;
        padding: 0.55rem 0.65rem;
        border-radius: 10px;
        font-size: 0.85rem;
        line-height: 1.35;
        width: 240px; /* approx 7x10cm style box */
        max-width: 260px;
        min-width: 220px;
        text-align: left;
        white-space: normal;
        word-break: normal;
        hyphens: auto;
        opacity: 0;
        pointer-events: none;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: opacity 0.15s ease, transform 0.15s ease;
        z-index: 20;
    }
    .help-dot:hover::after {
        opacity: 1;
        transform: translate(-50%, -4px);
    }
    .slider-label {
        font-weight: 800;
        color: var(--ink);
        margin-bottom: 0.35rem;
        display: block;
        font-size: 0.92rem;
    }
    .slider-card {
        background: linear-gradient(180deg, #fff6fb, #ffe9f4);
        border: 1px solid rgba(239, 199, 221, 0.9);
        border-radius: 14px;
        padding: 0.65rem 0.7rem 0.55rem 0.7rem;
        box-shadow: inset 0 0 8px rgba(200, 120, 190, 0.14);
    }
    /* --- INPUTS --- */
    label[data-baseweb="typography"], .stNumberInput label, .stSlider label {
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        color: var(--ink) !important;
        margin-bottom: 0.35rem;
    }
    .stNumberInput > div > div > input {
        background: #fff9fd !important;
        border-radius: 12px !important;
        border: 1px solid rgba(244, 160, 193, 0.7) !important;
        color: var(--ink) !important;
        font-weight: 600;
        padding: 0.55rem 0.75rem; 
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.08);
    }
    .stSlider > div > div { padding: 0.1rem 0 0.35rem 0; }
    /* --- BUTTON (CTA) --- */
    div.stButton > button {
        background: linear-gradient(145deg, #ff5fa2, #ff3f7f);
        color: white;
        border-radius: 14px;
        padding: 0.7rem 1.0rem;
        font-weight: 800;
        border: none;
        box-shadow: 0 12px 24px rgba(255, 99, 170, 0.35);
        transition: all 0.3s;
        font-size: 0.95rem;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 26px rgba(255, 99, 170, 0.45);
    }
    /* --- RIGHT COLUMN CONTAINER (Visual + Prediction) --- */
    .right-column-container {
        background: var(--panel);
        border-radius: 18px;
        padding: 1.05rem 0.9rem;
        box-shadow: inset 0 0 16px rgba(200, 150, 255, 0.2);
    }
    /* --- PREDICTION BOX (Cute) --- */
    .prediction-box {
        text-align: center;
        margin-top: 0.7rem;
        padding: 1.0rem 0.8rem;
        border-radius: 14px;
        box-shadow: 0 5px 14px rgba(106, 26, 122, 0.15);
        border: 1px solid rgba(220, 180, 255, 0.5);
        position: relative;
        overflow: hidden;
    }
    .status-text {
        font-size: 1.9rem; 
        font-weight: 900;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .text-regular { color: #3a9c4a; }
    .bg-regular { background: #e8ffe9; }
    .text-irregular { color: #ff4f9b; }
    .bg-irregular { background: #ffe7f4; } 
    .text-awaiting { color: var(--muted); }
    .bg-awaiting { background: var(--panel-2); }
    
    .sparkle-overlay::before, .sparkle-overlay::after {
        content: "✨";
        position: absolute;
        font-size: 1.2em;
        opacity: 0.7;
        color: #ffdd99; /* Gold sparkle color */
        animation: sparkle-float 6s infinite ease-in-out;
    }
    .sparkle-overlay::before { top: 10%; left: 5%; animation-delay: 0s; }
    .sparkle-overlay::after { bottom: 10%; right: 5%; animation-delay: 3s; }

    @keyframes sparkle-float {
        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.7; }
        50% { transform: translate(5px, -5px) scale(1.2); opacity: 1.0; }
    }
    .info-card {
        background: var(--panel-2);
        border-radius: 14px;
        padding: 0.65rem;
        border: 1px solid rgba(200, 160, 255, 0.4);
        color: var(--ink);
        font-size: 0.92rem;
        box-shadow: inset 0 0 10px rgba(200, 150, 255, 0.16);
        height: 100%;
    }

    /* --- FOOTER --- */
    .footnote {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 1.1rem;
        text-align: center;
        color: #552288;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- LOAD MODEL (Assuming gradient_boosting_cycle_classifier.pkl is in the same directory) ----------
try:
    model = joblib.load("gradient_boosting_cycle_classifier.pkl")
except FileNotFoundError:
    st.error("Model file not found. 💔")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()


# ---------- SMALL HELPERS (Phase logic updated) ----------
def infer_phase(day, cycle_length):
    """Accurate phase mapping for visualization."""
    ovulation_day_estimate = cycle_length - 14 
    if day <= 5:
        return "Menses", "🩸"
    elif day < ovulation_day_estimate:
        return "Follicular", "🌱"
    elif day == ovulation_day_estimate or day == ovulation_day_estimate + 1:
        return "Ovulation", "💖"
    else:
        return "Luteal", "🌙"


def draw_uterus_visual(phase, is_irregular):
    """
    Draw a stylized, sparkly, anatomically clearer uterus visual.
    

[Image of the female reproductive system with uterus]

    """
    fig, ax = plt.subplots(figsize=(3.0, 3.0)) 
    # lightweight "motion" tick to slightly move drops/eggs on rerun
    anim_tick = (time.time() % 4) / 4.0
    # Match the container background
    fig.patch.set_facecolor("#fff6fb")
    ax.set_facecolor("#fff6fb")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4, 4)
    ax.axis("off")

    # Dynamic Lining Thickness/Color (Soft pastel colors)
    if phase == "Menses":
        lining_color = "#ff88aa"  # Soft Red/Pink
        lining_height = 3.0 * 0.4 
        ovary_glow = "#ffc0d8"
    elif phase == "Follicular":
        lining_color = "#b3ffb3"  # Mint Green
        lining_height = 3.0 * 0.7 
        ovary_glow = "#aaffaa"
    elif phase == "Ovulation":
        lining_color = "#ffdd99"  # Sunny Yellow/Peach
        lining_height = 3.0 * 0.9 
        ovary_glow = "#ffb3d9"  
    else: # Luteal
        lining_color = "#d9b3ff"  # Lavender/Lilac
        lining_height = 3.0 * 0.8
        ovary_glow = "#e6ccff" 
    
    # --- SOFT GLOW / AURA (Micro-animation goal: gentle movement) ---
    # Soft halo around the organ block
    ax.add_patch(Ellipse(
        (0, 0.8), width=8.2, height=8.2, angle=0, edgecolor="none", 
        facecolor="#ffbad9", alpha=0.24, zorder=0
    ))
    
    # --- UTERUS BODY (Anatomically clearer, warmer palette) ---
    uterus_fill = "#f6a9bb"  # Rosy base
    uterus_border = "#df6f8a" # Deeper outline
    highlight_fill = "#ffd6e2"
    
    # Uterine Fundus + Body
    ax.add_patch(Ellipse(
        (0, 1.2), width=3.4, height=3.6, angle=0, edgecolor=uterus_border, 
        facecolor=uterus_fill, linewidth=2.0, alpha=1.0, zorder=1
    ))
    # Soft highlight in the center
    ax.add_patch(Ellipse(
        (0, 1.25), width=2.6, height=3.0, angle=0, edgecolor="none",
        facecolor=highlight_fill, alpha=0.65, zorder=1
    ))
    
    # --- ENDOMETRIAL LINING (Inner shape, dynamic thickness) ---
    ax.add_patch(Ellipse(
        (0, 1.2), width=1.8, height=lining_height, angle=0, edgecolor="none", 
        facecolor=lining_color, alpha=0.95, zorder=2
    ))
    
    # --- CERVIX/VAGINA ---
    cervix = plt.Rectangle(
        (-0.45, -3.05), 0.9, 1.4, facecolor=uterus_fill, edgecolor=uterus_border, linewidth=1.2, zorder=1
    )
    ax.add_patch(cervix)
    ax.plot([0,0], [-1.4, -2.7], color="#d46d7f", linewidth=1.1, zorder=3)

    # --- FALLOPIAN TUBES & OVARIES ---
    tube_color = "#e88fa2" # Soft warm pink
    
    # Tubes (Curved for a softer look)
    ax.plot([-1.5, -3.8], [2.3, 2.7], color=tube_color, linewidth=2.6, solid_capstyle='round', alpha=0.85, zorder=1)
    ax.plot([1.5, 3.8], [2.3, 2.7], color=tube_color, linewidth=2.6, solid_capstyle='round', alpha=0.85, zorder=1)

    # Ovaries (warmer tone, slight ellipse like the reference)
    ovary_size = 0.35 + (0.1 if phase == "Ovulation" else 0) 
    
    def draw_ovary(center_x, center_y, color):
        # Soft glow
        ax.add_patch(Ellipse((center_x, center_y), width=ovary_size*2.4, height=ovary_size*1.9, facecolor=color, alpha=0.32, zorder=0))
        # Main ovary body (warm amber/peach)
        ax.add_patch(Ellipse((center_x, center_y), width=ovary_size*1.9, height=ovary_size*1.6, facecolor="#f7b16f", edgecolor="#f0a45e", linewidth=1.5, zorder=5))
        ax.add_patch(Ellipse((center_x, center_y+0.08), width=ovary_size*1.2, height=ovary_size*0.8, facecolor="#ffd9a8", edgecolor="none", alpha=0.9, zorder=6))

    draw_ovary(-4.0, 2.8, ovary_glow)
    draw_ovary(4.0, 2.8, ovary_glow)

    # --- FINAL SPARKLES (Micro-animation goal: drifting sparkles) ---
    sparkle_coords = {
        (0, 3.5): 100, (-3, 1): 150, (3.5, 0): 80, 
        (-1.5, -1.5): 120, (2.5, 3.0): 180, (0.5, -3.5): 90
    }
    for (x, y), s in sparkle_coords.items():
        ax.scatter(x, y, s=s, color='#ffdd99', alpha=0.6, edgecolors='none', marker='*', zorder=6) 

    # --- PHASE VISUALS ---
    if phase == "Ovulation":
        # path of a traveling ovum from right ovary toward uterus
        egg_x = 4.0 - anim_tick * 3.2
        egg_y = 2.8 - anim_tick * 1.6
        ax.add_patch(Circle((egg_x, egg_y), radius=0.18, facecolor="#ffdd99", edgecolor="#ff66aa", linewidth=1.5, zorder=7))
        ax.scatter([3.7, 4.3, 4.5], [2.9, 3.1, 3.3], s=[150, 100, 70], color='#ffdd99', alpha=0.9, edgecolors='#ff66aa', linewidths=1.0, marker='*', zorder=6) 

    if phase == "Menses":
        # falling blood droplets to depict shedding
        drop_y_base = [-3.0, -3.3, -3.6]
        drop_x = [0.05, -0.25, 0.2]
        for i, y in enumerate(drop_y_base):
            drift = (i * 0.05) - 0.1
            fall = anim_tick * 0.7
            ax.scatter(drop_x[i] + drift, y - fall, s=90 - i*15, color="#ff2f7a", alpha=0.92, zorder=7, marker='o', edgecolors='white', linewidths=0.5)

    # Irregular Status Glow
    if is_irregular:
        glow_ring = Ellipse(
            (0, 1.2), width=4.5, height=4.5, angle=0, edgecolor="#ff66cc", 
            facecolor="none", linewidth=3, alpha=0.8, linestyle="--", zorder=10, 
        )
        ax.add_patch(glow_ring)

    return fig


# ---------- LAYOUT ----------
st.markdown("<div class='main-block'>", unsafe_allow_html=True)

# --- Fix 2: Clean Magical Gradient Header ---
st.markdown("<div class='header-gradient'></div>", unsafe_allow_html=True)


# Initialize state 
if 'is_irregular' not in st.session_state: st.session_state.is_irregular = False
if 'prediction_ran' not in st.session_state: st.session_state.prediction_ran = False
if 'label' not in st.session_state: st.session_state.label = "Ready for Vibe Check!" 
if 'msg' not in st.session_state: st.session_state.msg = "Plug in your magical stats and discover your cycle's secret!"
if 'pred_prob' not in st.session_state: st.session_state.pred_prob = None


# HEADER CONTENT ROW (Title and Subtitle)
header_content_col = st.columns(1)[0]
with header_content_col:
    st.markdown("<div class='title-text'>💖 Cycle Vibe Check ✨</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-text'>Predict regular vs irregular cycles and see today's phase—no scrolling required.</div>", unsafe_allow_html=True)
    
    # Fix 3: Status Badge under the title
    st.markdown(
        f"<div style='text-align: center; margin-bottom: 1.5rem;'><span class='header-status-badge'>STATUS: {st.session_state.label.upper()}</span></div>",
        unsafe_allow_html=True
    )

st.markdown("<div class='glow-divider'></div>", unsafe_allow_html=True)


# --- MAIN 2-COLUMN LAYOUT ---
predict_clicked = False

col_left, col_right = st.columns([1, 1.05]) 

# --- COLUMN LEFT: INPUTS (Cycle Inputs and Slider) ---
with col_left:
    st.markdown("<div class='section-label'>Profile</div>", unsafe_allow_html=True)
    st.markdown("<h3>💖 Your Cycle Snapshot</h3>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='field-label-row'>Cycle (days)"
            "<span class='help-dot' data-tip='Length from first day of your period to the day before the next. Typical range 21–35 days.'>?</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        cycle_length = st.number_input(
            "Cycle (days)",
            min_value=15, max_value=60, value=28, step=1, key="cycle_length_input",
            help="Typical cycle length is 21–35 days. Count from the first day of bleeding until the next period starts.",
            label_visibility="collapsed"
        )
    with c2:
        st.markdown(
            "<div class='field-label-row'>LH (mIU/mL)"
            "<span class='help-dot' data-tip='Luteinizing Hormone. Baseline often 1–12; surges 20–40+ about 24–36 hours before ovulation. Home LH strips or blood tests can measure this.'>?</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        lh_mean = st.number_input(
            "LH (mIU/mL)",
            value=6.0, min_value=1.0, max_value=30.0, step=0.1, key="lh_mean_input",
            help="Luteinizing Hormone. Home LH strips peak right before ovulation (often >20–40). Baseline can be 1–12.",
            label_visibility="collapsed"
        )
    with c3:
        st.markdown(
            "<div class='field-label-row'>Estrogen (pg/mL)"
            "<span class='help-dot' data-tip='Estradiol (E2). Rough ranges: ~30–100 early follicular, 150–300 just before ovulation, 60–200 luteal. Measured via blood tests.'>?</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        estrogen_mean = st.number_input(
            "Estrogen (pg/mL)",
            value=67.0, min_value=20.0, max_value=300.0, step=0.1, key="estrogen_mean_input",
            help="Estradiol (E2). Rough ranges: ~30–100 early follicular, 150–300 pre-ovulation, 60–200 luteal.",
            label_visibility="collapsed"
        )

    slider_col, action_col = st.columns([1.7, 1])
    with slider_col:
        st.markdown("<div class='section-label'>Today's spot in your cycle</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='field-label-row'>Simulate Day in Current Cycle"
            "<span class='help-dot' data-tip='Pick a day to see where you might be: days 1–5 menses, until ~(cycle length - 14) follicular, mid-cycle ovulation, later days luteal.'>?</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='slider-card'>", unsafe_allow_html=True)
        day_in_cycle = st.slider(
            "Simulate Day in Current Cycle",
            min_value=1, max_value=int(cycle_length), value=1, key="day_slider",
            label_visibility="collapsed",
            help="Choose a day to see where you might be: early days = menses, mid-cycle = ovulation, later = luteal."
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with action_col:
        st.markdown("<div class='section-label'>Run a quick check</div>", unsafe_allow_html=True)
        predict_clicked = st.button("Get My Cycle Vibe", use_container_width=True)
        st.caption("Updates instantly ➜")

    # Trigger prediction logic immediately on click
    if predict_clicked:
        X_new = np.array([[cycle_length, lh_mean, estrogen_mean]])
        pred = int(model.predict(X_new)[0])
        st.session_state.is_irregular = pred == 1 
        st.session_state.prediction_ran = True
        
        if st.session_state.is_irregular:
            st.session_state.label = "IRREGULAR 🌙" 
            st.session_state.msg = "Your cycle's vibe is a bit *variable*! Keep shining, but track your patterns closely."
        else:
            st.session_state.label = "REGULAR 👑"
            st.session_state.msg = "Looking wonderfully *consistent*! Your cycle is following a reliable, magic pattern."

        if hasattr(model, "predict_proba"):
            st.session_state.pred_prob = float(model.predict_proba(X_new)[0][pred])
        else:
            st.session_state.pred_prob = None

    # Result/Vibe box placed directly under inputs to avoid scrolling
    if st.session_state.prediction_ran:
        status_text = st.session_state.label.split(' ')[0] # REGULAR or IRREGULAR
        text_class = "text-" + status_text.lower()
        bg_class = "bg-" + status_text.lower()
    else:
        status_text = "VIBE PENDING"
        text_class = "text-awaiting"
        bg_class = "bg-awaiting"

    st.markdown("<div class='section-label'>Your vibe status</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='prediction-box {bg_class}'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='status-text {text_class}'>{status_text}</div>", 
        unsafe_allow_html=True
    )
    st.write(st.session_state.msg)
    if st.session_state.prediction_ran and st.session_state.pred_prob is not None:
        st.write(f"Magic Confidence: **{st.session_state.pred_prob:.2f}**")
        st.progress(min(max(st.session_state.pred_prob, 0.0), 1.0))
    st.markdown("</div>", unsafe_allow_html=True)

# --- COLUMN RIGHT: VISUAL + PREDICTION (The Magic Dashboard) ---
phase, phase_emoji = infer_phase(day_in_cycle, cycle_length)

with col_right:
    # Right column container holds visual and prediction box
    st.markdown("<div class='right-column-container'>", unsafe_allow_html=True)
    
    # 1. VISUAL + INFO SIDE BY SIDE
    phase_help = (
        "Phase vibe reflects the day you selected: Menses (days 1-5), "
        "Follicular (until ~14 days before period), Ovulation (mid-cycle surge), Luteal (post-ovulation)."
    )
    st.markdown(
        f"<h3 style='color: #4b1f3f; text-align: center; display: flex; align-items: center; gap: 0.4rem; justify-content: center;'>"
        f"✨ Phase Vibe: {phase.upper()} ({phase_emoji})"
        f"<span class='help-dot' data-tip='{phase_help}'>?</span>"
        f"</h3>",
        unsafe_allow_html=True,
    )
    
    fig_col, info_col = st.columns([1.05, 0.95])
    with fig_col:
        fig = draw_uterus_visual(phase, st.session_state.is_irregular)
        st.pyplot(fig, transparent=True, use_container_width=True)
    with info_col:
        st.markdown(
            "<div class='info-card'><b>CHECKING THE COSMIC CODE</b><br/>"
            "• Average Cycle Length<br/>"
            "• LH Levels (Ovulation Signal)<br/>"
            "• Estrogen Trends (Aura Balance)</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='info-card' style='margin-top: 0.4rem;'><b>YOUR MAGIC TIP</b><br/>"
            "If your last cycle was unexpected, try entering those stats to see how your aura changed!</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True) # close right-column-container


# --- Footer Disclaimer (Fix 5: Soft, magical Tone) ---
st.markdown(
    "<div class='footnote'>Just a friendly heads-up: This is a fun prototype! For medical advice, chat with your favorite healthcare professional and keep sparkling. ✨</div>",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
