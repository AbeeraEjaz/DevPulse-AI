import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from utils.data_preprocessor import clean_and_prepare_dataset
from utils.explainer import get_policy_feature_importance
from utils.simulator import PolicySimulatorEngine
from utils.report_generator import generate_policy_brief_pdf

# Page Configuration
st.set_page_config(
    page_title="DevPulse AI | UNDP Policy & HDI Simulator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (UN Blue & Clean Card Layouts)
st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .metric-card {
        background: #FFFFFF;
        padding: 18px 22px;
        border-radius: 12px;
        border-left: 5px solid #006EB5;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }
    .custom-title { color: #003366; font-weight: 800; font-size: 2.2rem; }
    .custom-subtitle { color: #475569; font-size: 1rem; margin-top: -10px; margin-bottom: 25px; }
    .footer-box {
        text-align: center;
        padding: 25px 10px;
        margin-top: 50px;
        border-top: 1px solid #E2E8F0;
        color: #64748B;
        font-size: 0.95rem;
    }
    .linkedin-btn {
        display: inline-block;
        background: #0A66C2;
        color: white !important;
        padding: 8px 18px;
        border-radius: 20px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.85rem;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Load Data and Simulator
@st.cache_data
def load_all():
    df = clean_and_prepare_dataset()
    importance_df, top_driver_text = get_policy_feature_importance()
    return df, importance_df, top_driver_text

with st.spinner("Initializing DevPulse AI Policy Intelligence Engine..."):
    df, importance_df, top_driver_text = load_all()
    simulator = PolicySimulatorEngine()

# Header
st.markdown('<div class="custom-title">🌐 DevPulse AI: Socio-Economic Policy & HDI Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subtitle">Predictive Modeling & Policy Simulation aligned with UNDP Human Development Frameworks</div>', unsafe_allow_html=True)

# Top KPI Metric Row
k1, k2, k3, k4 = st.columns(4)
latest_year = df['Year'].max()
latest_df = df[df['Year'] == latest_year]

k1.metric("🌍 Monitored Countries", df['Country'].nunique())
k2.metric("📅 Historical Timeline", f"{df['Year'].min()} - {latest_year}")
k3.metric("📈 Avg Global HDI", f"{latest_df['Calculated_HDI'].mean():.3f}")
k4.metric("💡 Top Policy Driver", importance_df.iloc[0]['Indicator'])

st.markdown("---")

# Main Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Country Diagnostic & Trends",
    "🎯 Policy Driver Analytics (XAI)",
    "🎛️ 'What-If' Policy Intervention Simulator",
    "📋 Raw Dataset Explorer"
])

# -------------------------------------------------------------
# TAB 1: Country Diagnostic & Trends
# -------------------------------------------------------------
with tab1:
    col_sel, col_stat = st.columns([1, 2])
    
    country_list = sorted(df['Country'].unique().tolist())
    default_idx = country_list.index("Pakistan") if "Pakistan" in country_list else 0
    
    with col_sel:
        selected_country = st.selectbox("Select Target Country:", country_list, index=default_idx)
        c_data = df[df['Country'] == selected_country].sort_values(by='Year')
        latest_c = c_data.iloc[-1]
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>📍 {selected_country} ({int(latest_c['Year'])})</h4>
            <p><b>HDI Score:</b> {latest_c['Calculated_HDI']:.3f} ({latest_c['HDI_Category']})</p>
            <p><b>GDP per Capita:</b> ${latest_c['GDP_Per_Capita_USD']:,.2f}</p>
            <p><b>Life Expectancy:</b> {latest_c['Life_Expectancy_Years']:.1f} years</p>
            <p><b>Internet Adoption:</b> {latest_c['Internet_Users_Pct']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col_stat:
        fig_hdi = px.line(
            c_data, x='Year', y='Calculated_HDI',
            title=f"📈 Historical HDI Trajectory: {selected_country}",
            markers=True, line_shape='spline',
            color_discrete_sequence=['#006EB5']
        )
        fig_hdi.update_layout(yaxis_range=[0.3, 1.0], height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_hdi, use_container_width=True)

    # Multi-indicator trend
    st.subheader(f"Historical Indicator Shifts for {selected_country}")
    fig_ind = go.Figure()
    fig_ind.add_trace(go.Scatter(x=c_data['Year'], y=c_data['Life_Expectancy_Years'], name="Life Expectancy (Years)", line=dict(color="#10B981")))
    fig_ind.add_trace(go.Scatter(x=c_data['Year'], y=c_data['Internet_Users_Pct'], name="Internet Access (%)", line=dict(color="#6366F1")))
    fig_ind.add_trace(go.Scatter(x=c_data['Year'], y=c_data['Access_to_Electricity_Pct'], name="Electricity Access (%)", line=dict(color="#F59E0B")))
    fig_ind.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), hovermode="x unified")
    st.plotly_chart(fig_ind, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: Explainable AI & Policy Priorities
# -------------------------------------------------------------
with tab2:
    st.subheader("🎯 What Drives National Human Development?")
    st.info(top_driver_text)

    col_chart, col_explain = st.columns([3, 2])
    
    with col_chart:
        fig_bar = px.bar(
            importance_df,
            x='HDI_Impact_Pct',
            y='Indicator',
            orientation='h',
            title="Feature Importance: Direct Contribution to HDI Outcomes (%)",
            color='HDI_Impact_Pct',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(yaxis=dict(autorange="reversed"), height=380, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_explain:
        st.markdown("### 🏛️ UN Policy Takeaway")
        st.markdown("""
        * **Human Capital Priority:** Foundational indicators like *Life Expectancy* and *Adult Literacy* have non-linear multiplier effects on overall development.
        * **Digital Inclusion as Catalyst:** Internet and digital access now rival traditional physical infrastructure in advancing socio-economic parity.
        * **Targeted Budgeting:** Allocating budgets directly to top-ranked levers yields higher HDI gains compared to general spending.
        """)

# -------------------------------------------------------------
# TAB 3: "What-If" Policy Simulator
# -------------------------------------------------------------
with tab3:
    st.subheader(f"🎛️ Simulate Policy Interventions for {selected_country}")
    st.caption("Adjust policy targets below to simulate projected HDI score and GDP per capita growth in real-time.")

    sim_country_data = df[df['Country'] == selected_country].sort_values(by='Year').iloc[-1]
    
    baseline = {
        'Literacy_Rate_Adult_Pct': float(sim_country_data['Literacy_Rate_Adult_Pct']),
        'Life_Expectancy_Years': float(sim_country_data['Life_Expectancy_Years']),
        'Access_to_Electricity_Pct': float(sim_country_data['Access_to_Electricity_Pct']),
        'Renewable_Energy_Pct': float(sim_country_data['Renewable_Energy_Pct']),
        'Internet_Users_Pct': float(sim_country_data['Internet_Users_Pct']),
        'Infant_Mortality_Rate': float(sim_country_data['Infant_Mortality_Rate'])
    }

    col_sliders1, col_sliders2 = st.columns(2)
    
    with col_sliders1:
        sim_lit = st.slider("Adult Literacy Rate (%)", 10.0, 100.0, baseline['Literacy_Rate_Adult_Pct'], 1.0)
        sim_life = st.slider("Life Expectancy (Years)", 40.0, 88.0, baseline['Life_Expectancy_Years'], 0.5)
        sim_elec = st.slider("Electricity Access (%)", 10.0, 100.0, baseline['Access_to_Electricity_Pct'], 1.0)

    with col_sliders2:
        sim_net = st.slider("Internet Adoption (%)", 5.0, 100.0, baseline['Internet_Users_Pct'], 1.0)
        sim_renew = st.slider("Renewable Energy Mix (%)", 0.0, 100.0, baseline['Renewable_Energy_Pct'], 1.0)
        sim_mort = st.slider("Infant Mortality Rate (per 1,000)", 2.0, 120.0, baseline['Infant_Mortality_Rate'], 1.0)

    simulated = {
        'Literacy_Rate_Adult_Pct': sim_lit,
        'Life_Expectancy_Years': sim_life,
        'Access_to_Electricity_Pct': sim_elec,
        'Renewable_Energy_Pct': sim_renew,
        'Internet_Users_Pct': sim_net,
        'Infant_Mortality_Rate': sim_mort
    }

    sim_res = simulator.simulate_impact(baseline, simulated)

    st.markdown("### 📊 Projected Policy Impact")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Current HDI", f"{sim_res['baseline_hdi']:.3f}")
    r2.metric("Projected HDI", f"{sim_res['simulated_hdi']:.3f}", delta=f"{sim_res['hdi_delta']:+.3f} ({sim_res['hdi_pct_change']:+0.1f}%)")
    r3.metric("Current GDP / Capita", f"${sim_res['baseline_gdp']:,.0f}")
    r4.metric("Projected GDP / Capita", f"${sim_res['simulated_gdp']:,.0f}", delta=f"${sim_res['gdp_delta']:+,.0f} ({sim_res['gdp_pct_change']:+0.1f}%)")

    # PDF Download Button
    st.markdown("---")
    if st.button("📄 Generate & Download Executive Policy Brief (PDF)"):
        with st.spinner("Rendering PDF Policy Report..."):
            pdf_path = generate_policy_brief_pdf(
                selected_country, baseline, simulated, sim_res, importance_df.iloc[0]['Indicator']
            )
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Click here to Download PDF",
                    data=f,
                    file_name=f"{selected_country}_UNDP_Policy_Brief.pdf",
                    mime="application/pdf"
                )

# -------------------------------------------------------------
# TAB 4: Raw Dataset Explorer
# -------------------------------------------------------------
with tab4:
    st.subheader("📋 Verified Global Development Indicators")
    st.dataframe(df, use_container_width=True)

# -------------------------------------------------------------
# Professional Footer (Branding & Verified LinkedIn Integration)
# -------------------------------------------------------------
# IMPORTANT: Replace YOUR_LINKEDIN_USERNAME with your actual LinkedIn profile handle
LINKEDIN_URL = "https://www.linkedin.com/in/abeera-ejaz-0b287a316?utm_source=share_via&utm_content=profile&utm_medium=member_android"
st.markdown(f"""
<style>
    .footer-box {{
        text-align: center;
        padding: 35px 20px 20px 20px;
        margin-top: 60px;
        border-top: 1px solid #E2E8F0;
        background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(241,245,249,0.6) 100%);
        border-radius: 0 0 16px 16px;
    }}
    .footer-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 4px;
    }}
    .footer-sub {{
        font-size: 0.9rem;
        color: #64748B;
        margin-bottom: 15px;
    }}
    .linkedin-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: #0A66C2;
        color: #FFFFFF !important;
        padding: 9px 22px;
        border-radius: 50px;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 0.88rem;
        box-shadow: 0 4px 14px rgba(10, 102, 194, 0.25);
        transition: all 0.25s ease-in-out;
    }}
    .linkedin-btn:hover {{
        background: #004182;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(10, 102, 194, 0.35);
        color: #FFFFFF !important;
    }}
    .linkedin-svg {{
        width: 17px;
        height: 17px;
        fill: #FFFFFF;
    }}
</style>

<div class="footer-box">
    <div class="footer-title">🌐 DevPulse AI — Global Socio-Economic Policy Simulator</div>
    <div class="footer-sub">Engineered with ❤️ by <b>Abeera Ejaz</b> | Final Year Computer Science Project</div>
    <a class="linkedin-btn" href="{LINKEDIN_URL}" target="_blank">
        <svg class="linkedin-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
        </svg>
        <span>Connect with Abeera Ejaz on LinkedIn</span>
    </a>
</div>
""", unsafe_allow_html=True)