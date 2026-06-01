import streamlit as st
from src.data_loader import load_data, apply_sidebar_filters
from src.data_processing import get_cgpa_band_summary, get_internship_summary, get_correlation_matrix
import src.visualizations as vis

st.set_page_config(page_title="Student Profiles", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found. Please run the data generator script.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='profiles')

st.title("Student Profile Analysis")
st.markdown("Understand how academic and skill factors affect outcomes.")

col1, col2 = st.columns(2)
with col1:
    cgpa_df = get_cgpa_band_summary(filtered_df)
    if not cgpa_df.empty:
        fig1 = vis.bar_chart(
            cgpa_df, x='cgpa_band', y='placement_rate',
            title="Placement Rate by CGPA Band", y_label="Placement Rate (%)", color_continuous=True
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Placement Rate by CGPA Band: Students are binned into CGPA ranges, and the percentage placed in each band is calculated. A clear upward trend validates CGPA as a strong predictor of placement success; the steepness indicates how much CGPA matters.")

with col2:
    int_df = get_internship_summary(filtered_df)
    if not int_df.empty:
        fig2 = vis.bar_chart(
            int_df, x='internships', y='placement_rate',
            title="Placement Rate by Internship Count", y_label="Placement Rate (%)"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Placement Rate by Internship Count: Groups students by number of completed internships. The marginal gain from each additional internship reveals whether experience is a differentiator or has diminishing returns.")

col3, col4 = st.columns(2)
with col3:
    # CGPA vs Package Scatter
    placed_df = filtered_df[filtered_df['outcome'] == 'Placed']
    if not placed_df.empty:
        fig3 = vis.scatter_plot(
            placed_df, x='cgpa', y='package_lpa',
            title="CGPA vs Package (LPA)", x_label="CGPA", y_label="Package (LPA)",
            trendline=True
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("CGPA vs Package: Each dot represents a placed student. The OLS trendline (dashed) shows the linear relationship between CGPA and compensation. R-squared of this fit indicates how much of salary variance is explained by academics alone.")
with col4:
    corr_df = get_correlation_matrix(filtered_df)
    if not corr_df.empty:
        fig4 = vis.correlation_heatmap(corr_df, title="Feature Correlation Heatmap")
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("Feature Correlation Heatmap: Pearson correlation coefficients between key numeric features and placement outcome (placed_flag). Strong positive correlations (dark blue) suggest predictive features for the ML model; near-zero values indicate weak signal.")

st.markdown("### CGPA Band Summary")
if not cgpa_df.empty:
    display_cols = {
        'cgpa_band': 'CGPA Band',
        'total_students': 'Students',
        'placed': 'Placed',
        'placement_rate': 'Placement Rate (%)',
        'higher_studies': 'Higher Studies',
        'unplaced': 'Unplaced'
    }
    st.dataframe(
        cgpa_df[display_cols.keys()].rename(columns=display_cols).style.format({
            'Placement Rate (%)': '{:.1f}'
        }),
        use_container_width=True, hide_index=True
    )
