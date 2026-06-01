import streamlit as st
import pandas as pd
from src.data_loader import load_data, apply_sidebar_filters
from src.data_processing import get_sector_summary
import src.visualizations as vis

st.set_page_config(page_title="Recruiter Segmentation", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='sector')

st.title("Recruiter Segmentation")
st.markdown("Classify recruiters by market segment and analyze sector demand.")

sector_df = get_sector_summary(filtered_df)

if not sector_df.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig1 = vis.bar_chart(sector_df, x='sector', y='total_offers', title="Sector-wise Hiring Volume")
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Sector-wise Hiring Volume: Total offers extended by companies in each industry sector. Dominant sectors reveal where institutional graduates are most in demand. Low-volume sectors may represent untapped opportunities for the placement cell.")
    with col2:
        fig2 = vis.bar_chart(sector_df, x='sector', y='avg_package', title="Sector-wise Average Package (LPA)")
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Sector-wise Average Package: Mean salary offered by each sector. High-paying sectors (e.g., Finance, Tech) attract top-CGPA students, while service sectors offer volume. This informs students about salary expectations by target industry.")
        
    col3, col4 = st.columns(2)
    with col3:
        # Branch preference by sector
        placed_df = filtered_df[filtered_df['outcome'] == 'Placed']
        cross = pd.crosstab(placed_df['branch'], placed_df['sector'])
        import plotly.graph_objects as go
        fig3 = go.Figure(go.Heatmap(
            z=cross.values, x=cross.columns, y=cross.index, colorscale='Blues',
            texttemplate='%{z}', textfont=dict(size=11)
        ))
        fig3.update_layout(title=dict(text="Branch Preference by Sector", font=dict(size=20, color='#111827')),
                           paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font=dict(size=14, color='#4B5563'), margin=dict(l=50, r=30, t=50, b=50))
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Branch Preference by Sector: Cross-tabulation of absolute hire counts per branch-sector pair. Dark cells show strong hiring affinity. CSE and IT branches tend to dominate Tech sectors, while ME and CE students are preferred in Core Engineering.")
    with col4:
        fig4 = vis.donut_chart(sector_df['sector'].tolist(), sector_df['num_recruiters'].tolist(), title="Recruiter Count by Sector")
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("Recruiter Count by Sector: Proportion of unique companies from each sector. A diverse sector mix reduces placement risk; over-reliance on a single sector makes the institution vulnerable to industry-specific downturns.")

    st.markdown("### Sector Summary Table")
    st.dataframe(sector_df, use_container_width=True, hide_index=True)
else:
    st.info("No placed data available for sector analysis.")
