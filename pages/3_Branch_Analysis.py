import streamlit as st
from src.data_loader import load_data, apply_sidebar_filters
from src.data_processing import get_branch_summary
import src.visualizations as vis

st.set_page_config(page_title="Branch Analysis", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found. Please run the data generator script.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='branch')

st.title("Branch Analysis")
st.markdown("Compare performance across different branches/departments.")

branch_df = get_branch_summary(filtered_df)

if not branch_df.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig1 = vis.bar_chart(
            branch_df.sort_values('placement_rate', ascending=True), 
            x='placement_rate', y='branch', horizontal=True,
            title="Placement Rate by Branch", text_auto=True, color_continuous=True
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Placement Rate by Branch: Percentage of students placed per department, sorted ascending. Color intensity maps to placement rate - darker bars indicate higher-performing branches. Compare against institutional average to identify under-performing departments.")
    with col2:
        fig2 = vis.bar_chart(
            branch_df.sort_values('median_package', ascending=True), 
            x='median_package', y='branch', horizontal=True,
            title="Median Package by Branch (LPA)", text_auto=True, color_continuous=True
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Median Package by Branch: The 50th percentile salary offered to placed students in each branch. Median is preferred over mean as it is robust to outlier offers (e.g., a single 40 LPA offer).")
        
    col3, col4 = st.columns(2)
    with col3:
        fig3 = vis.stacked_bar(
            branch_df, x='branch', 
            y_cols=['placed', 'higher_studies', 'unplaced'], 
            title="Outcome Distribution by Branch"
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Outcome Distribution by Branch: Stacked bars show absolute counts of Placed, Higher Studies, and Unplaced students per branch. Branches with taller 'Higher Studies' segments may reflect academic culture over industry readiness.")
    with col4:
        # Scatter of Placement Rate vs Median Package
        fig4 = vis.scatter_plot(
            branch_df, x='placement_rate', y='median_package',
            color_col='branch', size_col='total_students', text_col='branch',
            title="Placement Rate vs Median Package",
            x_label="Placement Rate (%)", y_label="Median Package (LPA)"
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("Placement Rate vs Median Package: Each bubble represents a branch; size encodes total student count. Branches in the top-right quadrant (high placement rate + high salary) represent the strongest departments. Outliers warrant deeper investigation.")

    st.markdown("### Branch Summary Table")
    display_cols = {
        'branch': 'Branch',
        'total_students': 'Students',
        'placed': 'Placed',
        'placement_rate': 'Placement Rate (%)',
        'median_package': 'Median Pkg (LPA)',
        'avg_package': 'Avg Pkg (LPA)',
        'avg_cgpa': 'Avg CGPA',
        'num_recruiters': 'Recruiters'
    }
    st.dataframe(
        branch_df[display_cols.keys()].rename(columns=display_cols).style.format({
            'Placement Rate (%)': '{:.1f}',
            'Median Pkg (LPA)': '{:.2f}',
            'Avg Pkg (LPA)': '{:.2f}',
            'Avg CGPA': '{:.2f}'
        }),
        use_container_width=True, hide_index=True
    )
