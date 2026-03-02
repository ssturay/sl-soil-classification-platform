import streamlit as st
from classification import classify_soil
from correlations import predict_cbr, predict_cu, predict_phi, subgrade_rating
from confidence import adjust_confidence

st.set_page_config(page_title="SL Soil Classification Tool", layout="centered")

st.title("Sierra Leone Regional Soil Classification & Prediction Tool")

st.sidebar.header("Input Parameters")

region = st.sidebar.selectbox("Region", ["West", "North", "South", "East"])

LL = st.sidebar.number_input("Liquid Limit (LL)", min_value=0.0, format="%.2f")
PL = st.sidebar.number_input("Plastic Limit (PL)", min_value=0.0, format="%.2f")
fines = st.sidebar.number_input("Fines (%)", min_value=0.0, max_value=100.0, format="%.2f")

sand = st.sidebar.number_input("Sand (%)", min_value=0.0, max_value=100.0, format="%.2f")
gravel = st.sidebar.number_input("Gravel (%)", min_value=0.0, max_value=100.0, format="%.2f")

N = st.sidebar.number_input("SPT N-value", min_value=0.0, format="%.2f")
MDD = st.sidebar.number_input("MDD (Mg/m³)", min_value=0.0, format="%.2f")
Gs = st.sidebar.number_input("Specific Gravity (Gs)", min_value=0.0, format="%.2f")

color = st.sidebar.selectbox("Soil Color", ["Unknown", "Red", "Reddish Brown", "Brown", "Other"])

if st.sidebar.button("Classify Soil"):

    # Convert zeros to None
    LL = LL if LL > 0 else None
    PL = PL if PL > 0 else None
    fines = fines if fines > 0 else None
    sand = sand if sand > 0 else None
    gravel = gravel if gravel > 0 else None
    N = N if N > 0 else None
    MDD = MDD if MDD > 0 else None
    Gs = Gs if Gs > 0 else None
    color = None if color == "Unknown" else color

    USCS, AASHTO, soil_group, PI, base_conf = classify_soil(
        LL, PL, fines, sand, gravel, Gs, color
    )

    CBR = predict_cbr(region, PI, MDD, N)
    Cu = predict_cu(region, PI, N)
    phi = predict_phi(region, sand, N)

    rating = subgrade_rating(CBR)

    final_conf = adjust_confidence(base_conf, N, MDD)

    st.subheader("Classification Results")

    st.write("USCS Class:", USCS)
    st.write("AASHTO Class:", AASHTO)
    st.write("Soil Group:", soil_group)

    st.subheader("Predicted Engineering Parameters")

    st.write("Plasticity Index (PI):", PI)
    st.write("CBR (%):", CBR)
    st.write("Undrained Shear Strength Cu (kPa):", Cu)
    st.write("Friction Angle φ (°):", phi)
    st.write("Subgrade Rating:", rating)

    st.subheader("Model Confidence")
    st.write(final_conf)
