import streamlit as st
import pandas as pd
from src.data_loader import load_data, apply_sidebar_filters
from src.metrics import branch_opportunity_index
import src.visualizations as vis

st.set_page_config(page_title="Branch Opportunity Index", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='boi')

st.title("Branch Opportunity Index")
st.markdown("Rank branches using a balanced scorecard model.")
st.markdown('''
The Branch Opportunity Index (BOI) is a composite weighted score (0-100) that ranks departments using multiple dimensions:
- **Placement Rate** and **Median Package** as primary performance indicators
- **Recruiter Count** and **Recruiter Diversity** as demand-side signals
- **Higher Studies Rate** and **Internship Conversion** as alternative outcome quality measures
- **Unplaced Rate** as a negative penalty factor

Adjust the weights in the sidebar to simulate different prioritization strategies.
''')

st.sidebar.markdown("### Index Weights")
w_placement = st.sidebar.slider("Placement Rate", 0.0, 1.0, 0.25)
w_package = st.sidebar.slider("Median Package", 0.0, 1.0, 0.20)
w_recruiters = st.sidebar.slider("Recruiter Count", 0.0, 1.0, 0.15)
w_diversity = st.sidebar.slider("Recruiter Diversity", 0.0, 1.0, 0.10)
w_higher = st.sidebar.slider("Higher Studies", 0.0, 1.0, 0.10)
w_internship = st.sidebar.slider("Internship Conversion", 0.0, 1.0, 0.10)
w_growth = st.sidebar.slider("Growth", 0.0, 1.0, 0.05)
w_unplaced = st.sidebar.slider("Unplaced Penalty", 0.0, 1.0, 0.05)

weights = {
    'placement_rate': w_placement,
    'median_package': w_package,
    'recruiter_count': w_recruiters,
    'recruiter_diversity': w_diversity,
    'higher_studies_rate': w_higher,
    'internship_conversion': w_internship,
    'growth': w_growth,
    'unplaced_penalty': w_unplaced
}

branches = filtered_df['branch'].unique()
scores = []
for branch in branches:
    branch_df = filtered_df[filtered_df['branch'] == branch]
    score = branch_opportunity_index(branch_df, weights)
    scores.append({'branch': branch, 'index_score': round(score, 1)})

scores_df = pd.DataFrame(scores).sort_values('index_score', ascending=False)

col1, col2 = st.columns(2)
with col1:
    fig1 = vis.bar_chart(scores_df, x='branch', y='index_score', title="Branch Opportunity Index", color_continuous=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Branch Opportunity Index: Composite score computed as a weighted sum of normalized placement rate, median package, recruiter count, sector diversity, higher studies rate, internship conversion, and an unplaced penalty. Branches scoring above 50 are considered strong performers under the current weighting scheme.")
with col2:
    st.markdown("### Index Scores")
    st.dataframe(scores_df, use_container_width=True, hide_index=True)
