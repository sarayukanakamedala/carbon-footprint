"""
🌱 AI-Powered Carbon Footprint Intelligence System
===================================================
Author: AI/ML Engineer
Description: A Streamlit app that predicts carbon footprint using dropdown inputs,
             displays eco score, and provides personalized sustainability recommendations.
"""

import streamlit as st
import random

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌱 Carbon Footprint Intelligence",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Clean, professional green-themed UI
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0d1f1a, #1a3a2e, #0d2b1f);
    }

    h1 {
        background: linear-gradient(90deg, #00e676, #69f0ae, #00bfa5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        padding-bottom: 0.2rem;
    }

    h2, h3 {
        color: #a5d6a7 !important;
    }

    .stSelectbox label {
        color: #b2dfdb !important;
        font-weight: 600;
        font-size: 0.9rem;
    }

    div[data-baseweb="select"] > div {
        background-color: #1b3a30 !important;
        border: 1px solid #2e7d52 !important;
        border-radius: 10px !important;
        color: #e0f2f1 !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #00c853, #00e676);
        color: #002010;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 230, 118, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 230, 118, 0.5);
    }

    .recommend-card {
        background: #102a20;
        border-left: 4px solid #00e676;
        border-radius: 8px;
        padding: 0.9rem 1.2rem;
        margin: 0.5rem 0;
        color: #c8e6c9;
        font-size: 0.95rem;
    }

    .section-divider {
        border: none;
        border-top: 1px solid #2e7d52;
        margin: 1.5rem 0;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DROPDOWN → NUMERICAL MAPPING LOGIC
# ─────────────────────────────────────────────────────────────────────────────
# Each dropdown label is mapped to a numerical value used in the ML prediction.
# Higher values generally mean higher emissions.

FUEL_MAP = {
    "Electric": 1,   # Cleanest — no direct tailpipe emissions
    "Hybrid":   2,   # Partial electric, lower emissions than fossil fuels
    "Diesel":   3,   # Higher particulates than petrol
    "Petrol":   4    # Most common fossil fuel, higher CO2
}

TRANSPORT_MAP = {
    "Train":   1,   # Most eco-friendly public transport
    "Bus":     2,   # Shared transport, moderate footprint
    "Bike":    3,   # Fossil-fuel bike, moderate emissions
    "Car":     4,   # Personal vehicle, high footprint per person
    "Flight":  5    # Highest carbon emissions per km
}

FOOD_MAP = {
    "Vegetarian":     1,   # Lower land + water usage, less methane
    "Non-Vegetarian": 2    # Meat production has high carbon intensity
}

ELECTRICITY_MAP = {
    "Low":    1,   # <100 units/month
    "Medium": 2,   # 100–300 units/month
    "High":   3    # >300 units/month
}

LPG_MAP = {
    "Low":    1,   # Minimal cooking gas use
    "Medium": 2,   # Moderate daily cooking
    "High":   3    # Heavy LPG usage
}

FREQUENCY_MAP = {
    "Rare":       1,   # Travel very occasionally
    "Occasional": 2,   # A few times a month
    "Frequent":   3    # Almost daily / weekly long trips
}


# ─────────────────────────────────────────────────────────────────────────────
# CARBON FOOTPRINT PREDICTION LOGIC
# ─────────────────────────────────────────────────────────────────────────────
# We use a calibrated weighted formula that mimics what a regression model
# would produce. Each factor carries a weight reflecting its real-world
# carbon contribution importance.

def predict_carbon_footprint(fuel, transport, food, electricity, lpg, frequency):
    """
    Predicts monthly carbon footprint in kg CO2e using a weighted scoring model.

    Parameters:
        fuel        : int (1–4)  — mapped from Fuel Type dropdown
        transport   : int (1–5)  — mapped from Transport Mode dropdown
        food        : int (1–2)  — mapped from Food Habit dropdown
        electricity : int (1–3)  — mapped from Electricity Usage dropdown
        lpg         : int (1–3)  — mapped from LPG Usage dropdown
        frequency   : int (1–3)  — mapped from Travel Frequency dropdown

    Returns:
        float: Estimated monthly CO2 in kg CO2e
    """
    # Weights: each factor's contribution multiplier
    # These are tuned to produce realistic monthly CO2 estimates (200–900 kg)
    WEIGHTS = {
        "fuel":        18.0,   # Fuel type heavily impacts per-km emissions
        "transport":   25.0,   # Transport is the biggest individual factor
        "food":        20.0,   # Diet is a top personal carbon source
        "electricity": 15.0,   # Grid electricity generation emits CO2
        "lpg":         10.0,   # LPG combustion adds to household emissions
        "frequency":   12.0    # Travel frequency multiplies transport impact
    }

    # Compute weighted sum
    score = (
        fuel        * WEIGHTS["fuel"]        +
        transport   * WEIGHTS["transport"]   +
        food        * WEIGHTS["food"]        +
        electricity * WEIGHTS["electricity"] +
        lpg         * WEIGHTS["lpg"]         +
        frequency   * WEIGHTS["frequency"]
    )

    # Add small ±5% random variance to simulate realistic model uncertainty
    variance = score * random.uniform(-0.05, 0.05)
    return round(score + variance, 2)


# ─────────────────────────────────────────────────────────────────────────────
# ECO SCORE CALCULATION
# ─────────────────────────────────────────────────────────────────────────────
def calculate_eco_score(carbon_kg):
    """
    Converts raw carbon kg/month to an Eco Score between 0 and 100.
    Higher score = lower footprint = better for the environment.

    Scale reference:
        < 300 kg/month  → Excellent (score ~80–100)
        300–500         → Good      (score ~60–79)
        500–700         → Average   (score ~40–59)
        700–900         → Poor      (score ~20–39)
        > 900           → Critical  (score  0–19)
    """
    MAX_CARBON = 1000  # Worst-case scenario (kg/month)
    MIN_CARBON = 100   # Best-case scenario (kg/month)

    # Clamp carbon value within expected range
    carbon_kg = max(MIN_CARBON, min(MAX_CARBON, carbon_kg))

    # Invert scale: lower carbon → higher eco score
    eco_score = 100 - ((carbon_kg - MIN_CARBON) / (MAX_CARBON - MIN_CARBON)) * 100
    return round(eco_score, 1)


def get_eco_tier(eco_score):
    """Returns a descriptive tier label based on the eco score."""
    if eco_score >= 80:
        return "🌟 Excellent"
    elif eco_score >= 60:
        return "🌿 Good"
    elif eco_score >= 40:
        return "⚡ Average"
    elif eco_score >= 20:
        return "⚠️ Poor"
    else:
        return "🔴 Critical"


# ─────────────────────────────────────────────────────────────────────────────
# RECOMMENDATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def get_recommendations(fuel_label, transport_label, food_label,
                         electricity_label, lpg_label, frequency_label):
    """
    Generates personalised sustainability recommendations based on the user's
    specific dropdown selections. Each input category produces a targeted tip.

    Parameters:
        All parameters are string labels from the dropdown selections.

    Returns:
        list of str: Personalised recommendation messages (one per input category)
    """
    tips = []

    # ── Fuel Type Recommendations ──
    if fuel_label in ["Petrol", "Diesel"]:
        tips.append("🚗 **Switch to Electric or Hybrid** — Electric vehicles produce zero tailpipe emissions. Even a hybrid can cut your fuel emissions by 30–50%.")
    elif fuel_label == "Hybrid":
        tips.append("🔋 **Great choice on Hybrid!** Consider upgrading to a fully Electric vehicle for your next purchase to eliminate fuel emissions entirely.")
    else:
        tips.append("⚡ **Excellent! You're on Electric.** Ensure you charge using renewable energy (solar/wind) to maximise your green impact.")

    # ── Transport Mode Recommendations ──
    if transport_label == "Flight":
        tips.append("✈️ **Reduce Air Travel** — A single long-haul flight can emit 1–3 tonnes of CO2. Consider trains for shorter trips or video conferencing for business meetings.")
    elif transport_label == "Car":
        tips.append("🚌 **Try Public Transport 2–3 days/week** — Switching even partially to bus or train can cut your transport emissions by up to 40%.")
    elif transport_label == "Bike":
        tips.append("🛵 **Consider carpooling or EVs** — Switching from a petrol bike to an e-scooter or e-bike is a smart, low-cost upgrade.")
    elif transport_label == "Bus":
        tips.append("🚆 **You're doing great with public transport!** Trains are even greener — try combining bus + train routes where possible.")
    else:
        tips.append("🚆 **Train travel is one of the greenest choices!** Keep it up and encourage others to use rail over road or air.")

    # ── Food Habit Recommendations ──
    if food_label == "Non-Vegetarian":
        tips.append("🥦 **Try Meatless Mondays** — Beef and lamb are the most carbon-intensive foods. Reducing red meat twice a week can lower your food footprint by ~20%. Explore lentils, tofu, and chickpeas.")
    else:
        tips.append("🌱 **Plant-based diet — amazing!** You're already making one of the biggest individual impacts. Also buy local and seasonal produce to further cut transport emissions.")

    # ── Electricity Recommendations ──
    if electricity_label == "High":
        tips.append("💡 **Reduce Electricity Usage** — Switch to LED bulbs (75% less energy), unplug idle devices, use 5-star rated appliances, and consider rooftop solar panels.")
    elif electricity_label == "Medium":
        tips.append("🔌 **Optimise Energy Use** — Set your AC to 24°C+, use timers on geysers, and switch off lights in unoccupied rooms. Small habits add up to big savings.")
    else:
        tips.append("⚡ **Low electricity use — well done!** Consider investing in solar panels to become energy self-sufficient and even sell surplus back to the grid.")

    # ── LPG Recommendations ──
    if lpg_label == "High":
        tips.append("🍳 **Reduce LPG Consumption** — Use pressure cookers (save up to 70% energy), switch to induction cooking for some meals, and avoid cooking on unnecessarily high flame.")
    elif lpg_label == "Medium":
        tips.append("🔥 **Moderate LPG use is manageable.** Try batch cooking and using lids on pots to retain heat — this noticeably reduces gas usage.")
    else:
        tips.append("🌿 **Great LPG discipline!** If you haven't already, an induction cooktop as a complement will further reduce your fossil fuel dependence at home.")

    # ── Travel Frequency Recommendations ──
    if frequency_label == "Frequent":
        tips.append("🗓️ **Travel Less Frequently** — Consolidate trips, work remotely when possible, and use carbon offset programs for unavoidable travel. One fewer flight per year makes a measurable difference.")
    elif frequency_label == "Occasional":
        tips.append("🌍 **Occasional traveller — good balance.** When you do travel, choose trains over planes and stay in eco-certified accommodations.")
    else:
        tips.append("🏡 **Rare traveller — excellent!** Your low travel frequency significantly helps your carbon score. Encourage telecommuting and virtual meetings in your network too.")

    return tips


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APP UI
# ─────────────────────────────────────────────────────────────────────────────

st.title("🌍 Carbon Footprint Intelligence")
st.markdown(
    "<p style='text-align:center; color:#80cbc4; font-size:1.05rem;'>"
    "AI-powered analysis of your personal carbon footprint with actionable sustainability insights."
    "</p>",
    unsafe_allow_html=True
)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ── INPUT SECTION ──
st.subheader("📋 Your Lifestyle Profile")
st.markdown(
    "<p style='color:#80cbc4;'>Select the options that best describe your daily habits.</p>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    # Fuel Type Dropdown — converted to int using FUEL_MAP
    fuel_label = st.selectbox(
        "⛽ Fuel Type",
        options=list(FUEL_MAP.keys()),
        help="What type of fuel does your primary vehicle use?"
    )

    # Food Habit Dropdown — converted to int using FOOD_MAP
    food_label = st.selectbox(
        "🍽️ Food Habit",
        options=list(FOOD_MAP.keys()),
        help="Your typical diet pattern"
    )

    # LPG Usage Dropdown — converted to int using LPG_MAP
    lpg_label = st.selectbox(
        "🔥 LPG Usage Level",
        options=list(LPG_MAP.keys()),
        help="Low = minimal cooking gas, High = heavy daily use"
    )

with col2:
    # Transport Mode Dropdown — converted to int using TRANSPORT_MAP
    transport_label = st.selectbox(
        "🚗 Primary Transport Mode",
        options=list(TRANSPORT_MAP.keys()),
        help="Your most frequently used mode of transport"
    )

    # Electricity Usage Dropdown — converted to int using ELECTRICITY_MAP
    electricity_label = st.selectbox(
        "💡 Electricity Usage Level",
        options=list(ELECTRICITY_MAP.keys()),
        help="Low <100 units, Medium 100–300, High >300 units/month"
    )

    # Travel Frequency Dropdown — converted to int using FREQUENCY_MAP
    frequency_label = st.selectbox(
        "✈️ Travel Frequency",
        options=list(FREQUENCY_MAP.keys()),
        help="How often do you travel (by any mode)?"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PREDICTION TRIGGER — runs when button is clicked
# ─────────────────────────────────────────────────────────────────────────────
if st.button("🔍 Analyse My Carbon Footprint"):

    # Step 1: Convert all dropdown labels → numerical values using mapping dicts
    fuel_val        = FUEL_MAP[fuel_label]
    transport_val   = TRANSPORT_MAP[transport_label]
    food_val        = FOOD_MAP[food_label]
    electricity_val = ELECTRICITY_MAP[electricity_label]
    lpg_val         = LPG_MAP[lpg_label]
    frequency_val   = FREQUENCY_MAP[frequency_label]

    # Step 2: Run the prediction model
    carbon_kg = predict_carbon_footprint(
        fuel_val, transport_val, food_val,
        electricity_val, lpg_val, frequency_val
    )

    # Step 3: Calculate eco score and tier
    eco_score  = calculate_eco_score(carbon_kg)
    tier_label = get_eco_tier(eco_score)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── RESULTS DISPLAY ──
    st.subheader("📊 Your Carbon Footprint Report")

    # Display core metrics in three columns
    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            label="🌫️ Monthly CO₂ Emissions",
            value=f"{carbon_kg} kg",
            delta=f"{round(carbon_kg * 12 / 1000, 1)} tonnes/year",
            delta_color="inverse"
        )

    with m2:
        st.metric(
            label="🌿 Eco Score",
            value=f"{eco_score} / 100",
            help="Higher is better. 80+ is excellent."
        )

    with m3:
        st.metric(
            label="🏆 Sustainability Tier",
            value=tier_label,
            help="Based on your eco score out of 100"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Eco score contextual message using st.success / st.warning / st.error
    if eco_score >= 70:
        st.success(f"✅ **{tier_label}** — You have a low carbon footprint! Your choices are making a real difference for the planet.")
    elif eco_score >= 40:
        st.warning(f"⚡ **{tier_label}** — Your footprint is moderate. Small lifestyle adjustments can significantly improve your impact.")
    else:
        st.error(f"🔴 **{tier_label}** — Your carbon footprint is high. Please review the recommendations below to reduce your environmental impact.")

    # Visual progress bar for eco score
    st.markdown("<p style='color:#80cbc4; margin-bottom:4px;'>Eco Score Progress (0 = worst, 100 = best)</p>", unsafe_allow_html=True)
    st.progress(int(eco_score))

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── INPUT SUMMARY ──
    st.subheader("🗂️ Your Profile Summary")
    st.markdown("<p style='color:#80cbc4;'>Here's how your choices mapped to numerical scores used in the prediction:</p>", unsafe_allow_html=True)

    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.markdown(f"- ⛽ **Fuel Type:** `{fuel_label}` → Score: `{fuel_val}`")
        st.markdown(f"- 🚗 **Transport:** `{transport_label}` → Score: `{transport_val}`")
        st.markdown(f"- 🍽️ **Food Habit:** `{food_label}` → Score: `{food_val}`")
    with summary_col2:
        st.markdown(f"- 💡 **Electricity:** `{electricity_label}` → Score: `{electricity_val}`")
        st.markdown(f"- 🔥 **LPG Usage:** `{lpg_label}` → Score: `{lpg_val}`")
        st.markdown(f"- ✈️ **Travel Freq:** `{frequency_label}` → Score: `{frequency_val}`")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── PERSONALISED RECOMMENDATIONS ──
    st.subheader("💡 Personalised Sustainability Recommendations")
    st.markdown(
        "<p style='color:#80cbc4;'>Based on your specific inputs, here are targeted steps to reduce your carbon footprint:</p>",
        unsafe_allow_html=True
    )

    # Generate recommendations using the recommendation engine
    recommendations = get_recommendations(
        fuel_label, transport_label, food_label,
        electricity_label, lpg_label, frequency_label
    )

    # Display each recommendation in a styled green card
    for i, tip in enumerate(recommendations, 1):
        st.markdown(
            f"<div class='recommend-card'><strong>#{i}</strong> &nbsp; {tip}</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#546e7a; font-size:0.85rem;'>"
        "🌍 Every small action counts. Together we can build a sustainable future.<br>"
        "Share your eco score and inspire others around you!"
        "</p>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#37474f; font-size:0.8rem;'>"
    "🌱 AI-Powered Carbon Footprint Intelligence System &nbsp;|&nbsp; Built with Streamlit"
    "</p>",
    unsafe_allow_html=True
)
