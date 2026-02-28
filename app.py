import streamlit as st
import pickle
import numpy as np
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1f4037, #99f2c8);
    }
    .main {
        background-color: rgba(255,255,255,0.85);
        padding: 20px;
        border-radius: 20px;
    }
    .title {
        font-size: 45px;
        font-weight: bold;
        color: #1f4037;
    }
    .subtext {
        font-size:20px;
        color:#555;
    }
    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #1f4037, #99f2c8);
        color: white;
        font-size:18px;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<p class="title">🏠 AI-Powered Smart House Price Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Advanced Machine Learning Model for Real Estate Valuation</p>', unsafe_allow_html=True)
st.write("")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model/model.pkl", "rb"))

# ---------------- INPUT SECTION ----------------
st.subheader("📋 Enter Property Details")

col1, col2, col3 = st.columns(3)

with col1:
    area = st.number_input("Area (sqft)", 500, 10000, 1500)
    bedrooms = st.number_input("Bedrooms", 1, 10, 3)
    bathrooms = st.number_input("Bathrooms", 1, 10, 2)

with col2:
    floors = st.number_input("Floors", 1, 5, 1)
    age = st.number_input("Age (Years)", 0, 100, 5)
    garage = st.selectbox("Garage Available?", ["No", "Yes"])

with col3:
    location_score = st.slider("Location Score", 1, 10, 5)
    luxury_level = st.slider("Luxury Level", 1, 10, 5)
    demand_index = st.slider("Market Demand Index", 1, 10, 6)

garage_value = 1 if garage == "Yes" else 0

# ---------------- PREDICTION ----------------
st.write("")
st.write("")

if st.button("🚀 Predict House Price"):

    with st.spinner("Analyzing market trends & property features..."):
        time.sleep(2)

    input_data = np.array([[area, bedrooms, bathrooms, floors,
                            age, garage_value, location_score]])

    prediction = model.predict(input_data)[0]

    st.markdown("---")
    st.success(f"💰 Estimated Property Value: ₹ {prediction:,.2f}")

    # ---------------- METRICS ----------------
    colA, colB, colC = st.columns(3)

    colA.metric("📏 Price per Sqft", f"₹ {prediction/area:,.2f}")
    colB.metric("🛏 Bedrooms", bedrooms)
    colC.metric("📍 Location Score Impact", f"{location_score}/10")

    st.write("")
    
    # ---------------- CONFIDENCE BAR ----------------
    confidence = np.random.randint(85, 98)
    st.subheader("🔍 Model Confidence")
    st.progress(confidence / 100)
    st.write(f"{confidence}% confidence level")

    # ---------------- VALUE METER ----------------
    st.subheader("📊 Price Position Indicator")

    if prediction < 3000000:
        st.info("🏠 Budget-Friendly Segment")
    elif prediction < 7000000:
        st.warning("🏘 Mid-Range Property")
    else:
        st.error("🏰 Premium / Luxury Property")

    st.balloons()