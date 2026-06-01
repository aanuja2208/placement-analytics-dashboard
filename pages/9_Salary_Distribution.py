import streamlit as st
import pandas as pd
from src.data_loader import load_data, apply_sidebar_filters
from src.utils import get_kpi_card_html, format_currency
import src.visualizations as vis

st.set_page_config(page_title="Salary Distribution", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='salary')
placed_df = filtered_df[filtered_df['outcome'] == 'Placed']

st.title("Salary Package Distribution")
st.markdown("Analyze compensation quality, variation, and outliers.")

if not placed_df.empty:
    # Summary stats
    stats = placed_df['package_lpa'].describe()
    iqr = stats['75%'] - stats['25%']
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(get_kpi_card_html("Highest Package", format_currency(stats['max'])), unsafe_allow_html=True)
    with c2: st.markdown(get_kpi_card_html("Average Package", format_currency(stats['mean'])), unsafe_allow_html=True)
    with c3: st.markdown(get_kpi_card_html("Median Package", format_currency(stats['50%'])), unsafe_allow_html=True)
    with c4: st.markdown(get_kpi_card_html("Lowest Package", format_currency(stats['min'])), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = vis.histogram(placed_df, 'package_lpa', title="Overall Package Distribution (LPA)")
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Overall Package Distribution: A frequency histogram of salary offers (LPA) with 30 bins. The shape reveals whether packages follow a normal distribution, are right-skewed (few high outliers), or bimodal (two distinct salary tiers from different company types).")
    with col2:
        fig2 = vis.box_plot(placed_df, 'branch', 'package_lpa', title="Package Distribution by Branch")
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Package Distribution by Branch: Box plots show the median (line), interquartile range (box), and outliers (dots) for each branch. Wider boxes indicate greater salary variance; outlier dots above the whiskers represent exceptionally high offers.")
        
    col3, col4 = st.columns(2)
    with col3:
        fig3 = vis.violin_plot(placed_df, 'company_type', 'package_lpa', title="Package Distribution by Company Type")
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Package Distribution by Company Type: Violin plots combine box plots with kernel density estimation, showing the full distribution shape. Wider regions indicate more students receiving packages in that range. Product companies typically show wider spreads at higher ranges.")
    with col4:
        # Yearly avg vs median
        yearly = placed_df.groupby('graduation_year')['package_lpa'].agg(['mean', 'median']).reset_index()
        fig4 = vis.line_chart(yearly, x='graduation_year', y=['mean', 'median'], title="Average vs Median Package Trend")
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("Average vs Median Package Trend: When the mean line diverges upward from the median, a few high-value outlier packages are inflating the average. The median provides a more representative measure of typical salary growth over time.")
        
    st.markdown("### Top 15 Highest Packages")
    top15 = placed_df.nlargest(15, 'package_lpa')[['student_id', 'branch', 'company_name', 'company_type', 'package_lpa']]
    st.dataframe(top15, use_container_width=True, hide_index=True)
else:
    st.info("No placed students found for the selected filters.")
