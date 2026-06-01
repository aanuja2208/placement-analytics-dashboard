import streamlit as st
import pandas as pd
from src.data_loader import load_data, apply_sidebar_filters
from src.metrics import get_executive_kpis
from src.data_processing import get_funnel_data
from src.utils import get_kpi_card_html, format_currency, format_percentage
import src.visualizations as vis

st.set_page_config(page_title="Executive Overview", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found. Please run the data generator script.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='exec')

st.title("Executive Overview")
st.markdown("High-level institutional summary of placement performance.")

kpis = get_executive_kpis(filtered_df)
if kpis:
    # Top Row
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(get_kpi_card_html("Total Students", kpis['total_students']), unsafe_allow_html=True)
    with c2: st.markdown(get_kpi_card_html("Placement Rate", format_percentage(kpis['placement_rate'])), unsafe_allow_html=True)
    with c3: st.markdown(get_kpi_card_html("Higher Studies Rate", format_percentage(kpis['higher_studies_rate'])), unsafe_allow_html=True)
    with c4: st.markdown(get_kpi_card_html("Unplaced Rate", format_percentage(kpis['unplaced_rate'])), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Second Row
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(get_kpi_card_html("Average Package", format_currency(kpis['avg_package'])), unsafe_allow_html=True)
    with c2: st.markdown(get_kpi_card_html("Median Package", format_currency(kpis['median_package'])), unsafe_allow_html=True)
    with c3: st.markdown(get_kpi_card_html("Highest Package", format_currency(kpis['highest_package'])), unsafe_allow_html=True)
    with c4: st.markdown(get_kpi_card_html("Total Recruiters", kpis['num_recruiters']), unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    outcome_counts = filtered_df['outcome'].value_counts()
    fig1 = vis.donut_chart(
        labels=outcome_counts.index.tolist(), 
        values=outcome_counts.values.tolist(), 
        title="Overall Outcome Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Outcome Distribution: Computed from the proportion of students in each outcome category (Placed, Higher Studies, Unplaced). A healthy institution typically shows 60%+ placement with 10-15% opting for higher studies.")

with col2:
    funnel_df = get_funnel_data(filtered_df)
    if not funnel_df.empty:
        fig2 = vis.funnel_chart(
            stages=funnel_df['stage'].tolist(), 
            values=funnel_df['count'].tolist(), 
            title="Placement Pipeline Funnel"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Placement Pipeline Funnel: Shows progressive attrition from total eligible students through registration, shortlisting, testing, interviews, and finally offer acceptance. Drop-off between stages highlights operational bottlenecks.")

col3, col4 = st.columns(2)

with col3:
    yearly = filtered_df.groupby('graduation_year').apply(lambda x: (x['outcome'] == 'Placed').mean() * 100, include_groups=False).reset_index(name='placement_rate')
    fig3 = vis.line_chart(yearly, x='graduation_year', y='placement_rate', title="10-Year Placement Rate Trend", y_label="Rate (%)")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("10-Year Placement Rate Trend: Calculated as (Placed / Total Students) x 100 for each graduation year. An upward trend indicates improving institutional placement effectiveness and industry demand.")

with col4:
    yearly_pkg = filtered_df[filtered_df['outcome'] == 'Placed'].groupby('graduation_year')['package_lpa'].mean().reset_index()
    fig4 = vis.bar_chart(yearly_pkg, x='graduation_year', y='package_lpa', title="Average Package Over Years", y_label="Package (LPA)")
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Average Package Over Years: Mean salary (in LPA) offered to placed students per year. Rising packages suggest better recruiter quality or improved student readiness; stagnation may indicate market saturation.")
