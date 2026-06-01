import streamlit as st
import pandas as pd
from src.data_loader import load_data, apply_sidebar_filters
from src.data_processing import get_yearly_summary
import src.visualizations as vis

st.set_page_config(page_title="Placement Trends", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found. Please run the data generator script.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='trends')

st.title("Placement Trends")
st.markdown("Year-over-year operational performance and trends.")

yearly_df = get_yearly_summary(filtered_df)

if not yearly_df.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig1 = vis.line_chart(
            yearly_df, x='year', 
            y=['placement_rate', 'higher_studies_rate', 'unplaced_rate'], 
            title="Outcome Rates by Year (%)"
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Outcome Rates by Year: Each line tracks the percentage of students in each outcome category per year. Convergence of lines suggests reducing variance in outcomes; divergence signals emerging disparities.")
    with col2:
        fig2 = vis.line_chart(
            yearly_df, x='year', 
            y=['avg_package', 'median_package'], 
            title="Salary Package Trends (LPA)"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Salary Package Trends: Mean and median package (LPA) computed from placed students only. When the mean significantly exceeds the median, it indicates a right-skewed distribution with a few very high offers pulling the average up.")

    col3, col4 = st.columns(2)
    with col3:
        fig3 = vis.bar_chart(
            yearly_df, x='year', y='num_recruiters', 
            title="Number of Recruiters by Year"
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Recruiter Participation: Count of unique companies that visited campus each year. Growth in recruiter count reflects the institution's expanding industry network and brand strength.")
    with col4:
        fig4 = vis.stacked_bar(
            yearly_df, x='year', 
            y_cols=['placed', 'higher_studies', 'unplaced'], 
            title="Outcome Distribution (Count)"
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("Outcome Distribution (Count): Absolute number of students in each outcome category per year, stacked to show total cohort size. Useful for identifying whether placement improvements are from fewer unplaced students or larger cohorts.")

    st.markdown("### Yearly Summary Table")
    display_cols = {
        'year': 'Year',
        'total_students': 'Total Students',
        'placed': 'Placed',
        'higher_studies': 'Higher Studies',
        'unplaced': 'Unplaced',
        'placement_rate': 'Placement Rate (%)',
        'avg_package': 'Avg Package (LPA)',
        'median_package': 'Median Package (LPA)',
        'num_recruiters': 'Recruiters'
    }
    st.dataframe(
        yearly_df[display_cols.keys()].rename(columns=display_cols).style.format({
            'Placement Rate (%)': '{:.1f}',
            'Avg Package (LPA)': '{:.2f}',
            'Median Package (LPA)': '{:.2f}'
        }),
        use_container_width=True, hide_index=True
    )
