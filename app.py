import streamlit as st
import pandas as pd
from recommend import get_sustainable_recommendations

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Smart Sustainable Shopping Recommender",
    page_icon="🌱",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── ROOT TOKENS ── */
:root {
    --bg-void:       #030a06;
    --bg-deep:       #060f09;
    --bg-card:       #0a1a0e;
    --bg-card-hover: #0e2214;
    --border-dim:    rgba(52, 211, 106, 0.10);
    --border-glow:   rgba(52, 211, 106, 0.30);
    --glow-green:    #34d36a;
    --glow-teal:     #2dd4bf;
    --glow-lime:     #a3e635;
    --accent-warm:   #f97316;
    --text-primary:  #e8f5ee;
    --text-muted:    #5e8a6a;
    --bad-red:       #ff4444;
    --radius-card:   20px;
    --radius-pill:   999px;
    --font-display:  'Syne', sans-serif;
    --font-mono:     'DM Mono', monospace;
}

/* ── GLOBAL RESET ── */
html, body, [class*="css"] {
    background-color: var(--bg-void) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
}

/* Animated noise + radial glow background */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 60% 50% at 15% 20%, rgba(52, 211, 106, 0.07) 0%, transparent 70%),
        radial-gradient(ellipse 40% 60% at 85% 75%, rgba(45, 212, 191, 0.05) 0%, transparent 70%),
        var(--bg-void);
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-void); }
::-webkit-scrollbar-thumb {
    background: var(--glow-green);
    border-radius: 3px;
}

/* ── MAIN TITLE ── */
.main-title {
    font-family: var(--font-display);
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 8px;
    color: var(--text-primary);
    position: relative;
}

.main-title span.accent {
    background: linear-gradient(100deg, var(--glow-green), var(--glow-teal), var(--glow-lime));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.title-eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--glow-green);
    margin-bottom: 12px;
    display: block;
    opacity: 0.8;
}

.title-divider {
    width: 64px;
    height: 3px;
    background: linear-gradient(90deg, var(--glow-green), var(--glow-teal));
    border-radius: 2px;
    margin: 20px 0 40px 0;
    box-shadow: 0 0 12px rgba(52, 211, 106, 0.5);
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-top: 48px;
    margin-bottom: 20px;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-glow), transparent);
    margin-left: 8px;
}

/* ── PRODUCT CARD ── */
.product-card {
    background: var(--bg-card);
    padding: 32px 36px;
    border-radius: var(--radius-card);
    margin-bottom: 20px;
    border: 1px solid var(--border-dim);
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
}

.product-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(52, 211, 106, 0.03) 0%, transparent 60%);
    pointer-events: none;
}

.product-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--glow-green), var(--glow-teal));
    border-radius: 3px 0 0 3px;
    opacity: 0.7;
}

.product-card:hover {
    border-color: var(--border-glow);
    box-shadow:
        0 0 0 1px rgba(52, 211, 106, 0.08),
        0 20px 60px rgba(0, 0, 0, 0.5),
        0 0 40px rgba(52, 211, 106, 0.04);
}

.product-card h1 {
    font-family: var(--font-display) !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin-bottom: 20px !important;
    letter-spacing: -0.5px;
}

.product-card p {
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
    color: var(--text-muted) !important;
    margin: 8px 0 !important;
    display: flex;
    gap: 8px;
}

.product-card p b {
    color: rgba(232, 245, 238, 0.5) !important;
    font-weight: 500;
    min-width: 80px;
    font-family: var(--font-mono) !important;
}

/* ── METRIC CARD ── */
.metric-card {
    background: var(--bg-card);
    padding: 24px 16px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 12px;
    border: 1px solid var(--border-dim);
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}

.metric-card::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--glow-teal), var(--glow-green), var(--glow-lime));
    opacity: 0.6;
}

.metric-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-glow);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.4), 0 0 20px rgba(52, 211, 106, 0.06);
}

.metric-card h3 {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    font-weight: 400 !important;
    margin-bottom: 10px !important;
}

.metric-card h1 {
    font-family: var(--font-display) !important;
    font-size: 34px !important;
    font-weight: 800 !important;
    color: var(--glow-green) !important;
    text-shadow: 0 0 20px rgba(52, 211, 106, 0.4);
    margin: 0 !important;
}

/* ── SUSTAINABILITY RESULT ── */
.good {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 22px;
    color: var(--glow-green);
    display: inline-flex;
    align-items: center;
    gap: 12px;
    padding: 18px 28px;
    background: rgba(52, 211, 106, 0.07);
    border: 1px solid rgba(52, 211, 106, 0.25);
    border-radius: var(--radius-card);
    box-shadow: 0 0 30px rgba(52, 211, 106, 0.08), inset 0 1px 0 rgba(52, 211, 106, 0.1);
    letter-spacing: -0.3px;
    width: 100%;
}

.bad {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 22px;
    color: var(--bad-red);
    display: inline-flex;
    align-items: center;
    gap: 12px;
    padding: 18px 28px;
    background: rgba(255, 68, 68, 0.07);
    border: 1px solid rgba(255, 68, 68, 0.25);
    border-radius: var(--radius-card);
    box-shadow: 0 0 30px rgba(255, 68, 68, 0.06), inset 0 1px 0 rgba(255, 68, 68, 0.1);
    letter-spacing: -0.3px;
    width: 100%;
}

/* ── BUTTONS ── */
.stButton > button {
    font-family: var(--font-display) !important;
    background: transparent !important;
    color: var(--glow-green) !important;
    border: 1px solid rgba(52, 211, 106, 0.4) !important;
    border-radius: 12px !important;
    padding: 12px 32px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.25s ease !important;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(52, 211, 106, 0.12), rgba(45, 212, 191, 0.06));
    opacity: 0;
    transition: opacity 0.25s;
}

.stButton > button:hover {
    border-color: var(--glow-green) !important;
    color: #ffffff !important;
    box-shadow:
        0 0 0 1px rgba(52, 211, 106, 0.3),
        0 0 24px rgba(52, 211, 106, 0.2),
        0 4px 20px rgba(0, 0, 0, 0.4) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:hover::before {
    opacity: 1;
}

/* ── DROPDOWNS / SELECTBOX ── */
div[data-baseweb="select"] > div {
    background-color: var(--bg-card) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border-dim) !important;
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
    transition: border-color 0.2s;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: var(--border-glow) !important;
    box-shadow: 0 0 0 3px rgba(52, 211, 106, 0.08) !important;
}

div[data-baseweb="select"] svg { color: var(--glow-green) !important; }

/* Dropdown list */
[data-baseweb="popover"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

[role="option"] {
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
    transition: background 0.15s;
}

[role="option"]:hover {
    background: rgba(52, 211, 106, 0.08) !important;
}

/* ── LABELS ── */
label, .stSelectbox label {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-muted) !important;
}

/* ── WARNINGS ── */
[data-testid="stAlert"] {
    background: rgba(163, 230, 53, 0.06) !important;
    border: 1px solid rgba(163, 230, 53, 0.2) !important;
    border-radius: 12px !important;
    color: var(--glow-lime) !important;
    font-family: var(--font-mono) !important;
}

/* ── COLUMN GAPS ── */
[data-testid="column"] { padding: 0 8px !important; }

/* ── HIDE STREAMLIT BRANDING ── */
#MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }

/* ── REC CARD VARIANT (slightly different accent) ── */
.product-card.rec::after {
    background: linear-gradient(180deg, var(--glow-teal), var(--glow-lime));
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

DATA_PATH = "data/cleaned_dataset.csv"

df = pd.read_csv(DATA_PATH)

# ---------------- ECO SCORE FUNCTION ---------------- #

def generate_eco_score(label):

    label = str(label).lower()

    if "organic" in label:
        return 95

    elif "eco" in label:
        return 90

    elif "recycled" in label:
        return 85

    elif "sustainable" in label:
        return 75

    else:
        return 40

# ---------------- RECYCLABILITY ---------------- #

def recyclability(score):

    if score >= 85:
        return "High"

    elif score >= 65:
        return "Medium"

    else:
        return "Low"

# ---------------- SUSTAINABILITY CHECK ---------------- #

def is_sustainable(score):

    return score >= 70

# ---------------- HEADER ---------------- #

st.markdown(
    """
    <span class="title-eyebrow">↯ Powered by Eco Intelligence</span>
    <div class="main-title">
        Smart <span class="accent">Sustainable</span><br>Shopping Recommender
    </div>
    <div class="title-divider"></div>
    """,
    unsafe_allow_html=True
)

# ---------------- CATEGORY SELECTION ---------------- #

categories = sorted(df["category"].dropna().unique())

selected_category = st.selectbox(
    "📂 Select Category",
    categories
)

# ---------------- PRODUCT SELECTION ---------------- #

filtered_products = df[
    df["category"] == selected_category
]

product_names = sorted(
    filtered_products["product_name"].dropna().unique()
)

selected_product = st.selectbox(
    "📦 Select Product",
    product_names
)

# ---------------- BUTTON ---------------- #

analyze = st.button("↗ Analyze Product")

# ---------------- ANALYSIS ---------------- #

if analyze:

    product = df[
        df["product_name"] == selected_product
    ].iloc[0]

    eco_score = generate_eco_score(
        product["sustainability_label"]
    )

    recycle = recyclability(eco_score)

    sustainable = is_sustainable(eco_score)

    # ---------- PRODUCT DETAILS ---------- #

    st.markdown(
        """
        <div class="section-title">
            📦 Product Details
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        st.markdown(
            f"""
            <div class="product-card">

            <h1>{product['product_name']}</h1>

            <p><b>Category</b> {product['category']}</p>

            <p><b>Material</b> {product['material']}</p>

            <p><b>Brand</b> {product['brand']}</p>

            <p><b>Country</b> {product['country_of_origin']}</p>

            <p><b>Price</b> ${product['price_usd']}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
            <h3>⭐ Rating</h3>
            <h1>{product['rating']}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="metric-card">
            <h3>🌱 Eco Score</h3>
            <h1>{eco_score}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="metric-card">
            <h3>♻️ Recyclability</h3>
            <h1>{recycle}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- SUSTAINABILITY RESULT ---------- #

    st.markdown(
        """
        <div class="section-title">
            🌿 Sustainability Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    if sustainable:

        st.markdown(
            """
            <div class="good">
                ✅ This product is SUSTAINABLE
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="bad">
                ❌ This product is NOT SUSTAINABLE
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- RECOMMENDATIONS ---------- #

    recommendations = get_sustainable_recommendations(
        df,
        selected_product
    )

    st.markdown(
        """
        <div class="section-title">
            ♻️ Recommended Eco-Friendly Alternatives
        </div>
        """,
        unsafe_allow_html=True
    )

    if recommendations.empty:

        st.warning("No recommendations found.")

    else:

        for _, row in recommendations.iterrows():

            rec_score = generate_eco_score(
                row["sustainability_label"]
            )

            rec_recycle = recyclability(rec_score)

            st.markdown(
                f"""
                <div class="product-card rec">

                <h1>{row['product_name']}</h1>

                <p><b>Category</b> {row['category']}</p>

                <p><b>Brand</b> {row['brand']}</p>

                <p><b>Material</b> {row['material']}</p>

                <p><b>Eco Score</b> {rec_score}</p>

                <p><b>Rating</b> {row['rating']}</p>

                <p><b>Recyclability</b> {rec_recycle}</p>

                </div>
                """,
                unsafe_allow_html=True
            )