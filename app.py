import streamlit as st
import os

st.set_page_config(
    page_title="Campus Placement Analytics",
    page_icon="bar-chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path, 'r') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    # Basic CSS if file not found
    st.markdown("""
    <style>
        .stMetric {
            background-color: #1E2330;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 10px 15px;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Campus Placement Analytics")
st.markdown("""
### Production & Operations Management Edition

Welcome to the comprehensive placement analytics system. 
This dashboard treats the placement process as an operations supply chain, analyzing:
- **Throughput & Yield:** Placement rates and offer conversions
- **Quality & Variation:** Salary distributions and profiles
- **Demand Planning:** Recruiter analytics and forecasting
- **Resource Readiness:** Student outcome predictors and recommendations

Please select a module from the sidebar to begin.
""")

st.info("Select a page from the sidebar to analyze the data.")

# Main app entry point doesn't need much logic, pages handle themselves.
