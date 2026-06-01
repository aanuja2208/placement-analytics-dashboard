import streamlit as st
import pandas as pd
from src.data_loader import load_data, apply_sidebar_filters
from src.data_processing import get_cohort_summary, add_derived_columns
import src.visualizations as vis

st.set_page_config(page_title="Cohort Comparison", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='cohort')

st.title("Cohort Comparison Analysis")
st.markdown("Compare performance of different student batches (cohorts).")

group_by = st.selectbox("Compare cohorts by:", ['graduation_year', 'branch', 'major_project_domain'])

cohort_df = get_cohort_summary(filtered_df, group_cols=[group_by])

if not cohort_df.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig1 = vis.bar_chart(
            cohort_df.sort_values(group_by), x=group_by, y='placement_rate',
            title=f"Placement Rate by {group_by.replace('_', ' ').title()}", y_label="Placement Rate (%)"
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Placement Rate by Cohort: Compares the percentage of students placed across the selected grouping dimension. Variations across cohorts highlight systemic differences in outcomes that may be driven by curriculum, market conditions, or student preparation levels.")
    with col2:
        fig2 = vis.stacked_bar(
            cohort_df.sort_values(group_by), x=group_by,
            y_cols=['placed', 'higher_studies', 'unplaced'],
            title=f"Outcome Distribution by {group_by.replace('_', ' ').title()}"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Outcome Distribution by Cohort: Absolute counts of each outcome category per cohort, stacked for visual comparison. Proportional changes across cohorts reveal whether improvements are absolute (more students placed) or relative (smaller cohort sizes).")

    col3, col4 = st.columns(2)
    with col3:
        fig3 = vis.scatter_plot(
            cohort_df, x='avg_internships', y='placement_rate', text_col=group_by,
            title="Avg Internships vs Placement Rate", size_col='total_students',
            x_label="Avg Internships", y_label="Placement Rate (%)"
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Avg Internships vs Placement Rate: Each point represents a cohort; bubble size encodes cohort size. A positive correlation validates the hypothesis that practical experience drives placement success across cohorts.")
    with col4:
        # Cross tab heatmap for year vs branch if grouping by year
        if group_by == 'graduation_year':
            df_derived = add_derived_columns(filtered_df)
            cross = pd.crosstab(df_derived['branch'], df_derived['graduation_year'], values=df_derived['placed_flag'], aggfunc='mean') * 100
            cross = cross.fillna(0)
            import plotly.graph_objects as go
            fig4 = go.Figure(go.Heatmap(
                z=cross.values, x=cross.columns, y=cross.index, colorscale='Blues',
                texttemplate='%{z:.1f}%', textfont=dict(size=11)
            ))
            fig4.update_layout(title=dict(text="Placement Rate Heatmap (Branch x Year)", font=dict(size=20, color='#111827')),
                           paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           font=dict(size=14, color='#4B5563'), margin=dict(l=50, r=30, t=50, b=50))
            st.plotly_chart(fig4, use_container_width=True)
            st.caption("Placement Rate Heatmap (Branch x Year): Cross-tabulation showing placement rate for each branch in each year. Darker cells indicate higher placement rates. Useful for spotting branches with consistently strong or weak performance over time.")
        else:
            fig4 = vis.bar_chart(cohort_df, x=group_by, y='median_package', title=f"Median Package by {group_by.replace('_', ' ').title()}")
            st.plotly_chart(fig4, use_container_width=True)
            st.caption("Median Package by Cohort: The 50th percentile salary for placed students in each cohort. Comparing medians across cohorts reveals whether compensation quality is keeping pace with placement quantity.")

    st.markdown("### Cohort Summary Table")
    st.dataframe(cohort_df, use_container_width=True, hide_index=True)
