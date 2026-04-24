import streamlit as st
import json

# --- Load Database ---
try:
    with open('formulas.json', 'r') as f:
        formula_db = json.load(f)
except FileNotFoundError:
    st.error("formulas.json not found. Please ensure it is in the same directory.")
    formula_db = {}

st.set_page_config(page_title="UCH Formula Calculator", layout="wide")
st.title("🏥 Clinical Nutritional Intake Calculator")

# --- Inputs ---
st.sidebar.header("Patient Data")
weight = st.sidebar.number_input("Infant Weight (kg)", min_value=0.5, value=3.5, step=0.1)

st.header("1. Selection & Preparation")
col1, col2 = st.columns(2)

with col1:
    selected_name = st.selectbox("Select Formula Product", list(formula_db.keys()))
    product = formula_db[selected_name]
    
    # Handle RTF vs Powder
    is_rtf = product.get("is_rtf", False)
    if is_rtf:
        st.info(f"**{selected_name}** is a Ready-to-Feed (RTF) product.")
    else:
        st.success(f"**{selected_name}** is a powder formula.")

with col2:
    if is_rtf:
        total_daily_vol = st.number_input("Total volume consumed today (ml)", value=500)
    else:
        scoops = st.number_input("Scoops per feed", value=3.0, step=0.5)
        water = st.number_input("Water per feed (ml)", value=90.0)
        feeds = st.number_input("Number of feeds per day", value=8)

# --- Calculations ---
displacement = 0.75 

if is_rtf:
    daily_vol = total_daily_vol
    daily_kcal = (product['kcal_100ml'] / 100) * daily_vol
    daily_pro = (product['pro_100ml'] / 100) * daily_vol
else:
    powder_g = scoops * product['scoop_g']
    vol_per_feed = water + (powder_g * displacement)
    daily_vol = vol_per_feed * feeds
    # Nutritional value based on concentration
    daily_kcal = (product['kcal_100ml'] / 100) * daily_vol
    daily_pro = (product['pro_100ml'] / 100) * daily_vol

pe_ratio = (daily_pro / daily_kcal) * 100

# --- Results ---
st.divider()
st.subheader("Daily Nutritional Totals")
r1, r2, r3 = st.columns(3)
r1.metric("Total Energy", f"{daily_kcal:.0f} kcal")
r2.metric("Total Protein", f"{daily_pro:.1f} g")
r3.metric("P/E Ratio", f"{pe_ratio:.2f} g/100kcal")

st.subheader("Intake per Kilogram (per day)")
k1, k2, k3 = st.columns(3)
k1.metric("Energy/kg", f"{daily_kcal/weight:.1f} kcal/kg")
k2.metric("Protein/kg", f"{daily_pro/weight:.2f} g/kg")
k3.metric("Fluid/kg", f"{daily_vol/weight:.1f} ml/kg")
