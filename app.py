st.markdown("""
<style>
/* Arka planı açık gri/platin tonu yapalım */
.stApp {
    background: #f4f4f9;
}

/* Tüm ana metinler koyu gri/siyah olsun */
body, p, span, div, label, .stMarkdown, .stText {
    color: #2e2e2e !important;
}

.big-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 3.2rem;
    text-align: center;
    color: #1a1a1a;
    letter-spacing: 4px;
    margin-bottom: 0.1rem;
}

.sub {
    text-align: center;
    color: #555555;
    letter-spacing: 2px;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
}

/* Kartları aydınlık modda belirginleştirelim */
.card {
    border-radius: 12px;
    padding: 14px 20px;
    margin: 6px 0 2px 0;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    border: 1px solid #dcdcdc;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Roast kutularını hafif sarı/beyaz ton yapalım */
.roast {
    font-style: italic;
    font-size: 0.88rem;
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    border-left: 3px solid #ffcc00;
    background: #fffdf0;
    color: #333 !important;
}

.prob-row {
    padding: 12px 16px;
    margin: 6px 0;
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #eeeeee;
}

.section-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.6rem;
    color: #1a1a1a;
    letter-spacing: 2px;
    margin-top: 1.2rem;
    margin-bottom: 0.3rem;
}

/* Metrik kutuları */
div[data-testid="metric-container"] {
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
    padding: 10px;
}
div[data-testid="metric-container"] label {
    color: #666666 !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #000000 !important;
}

/* Sidebar aydınlık mod */
section[data-testid="stSidebar"] {
    background: #f0f2f6;
    border-right: 1px solid #dcdcdc;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #cccccc !important;
}
</style>
""", unsafe_allow_html=True)
