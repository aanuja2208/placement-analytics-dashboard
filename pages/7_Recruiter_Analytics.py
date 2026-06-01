import streamlit as st
from src.data_loader import load_data, apply_sidebar_filters
from src.data_processing import get_company_summary
from src.metrics import repeat_recruiter_rate, offer_acceptance_rate
from src.utils import get_kpi_card_html, format_percentage, format_currency
import src.visualizations as vis

st.set_page_config(page_title="Recruiter Analytics", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='recruiter')

st.title("Recruiter Analytics")
st.markdown("Analyze company hiring patterns, demand sources, and offer conversions.")

company_df = get_company_summary(filtered_df)

if not company_df.empty:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(get_kpi_card_html("Total Recruiters", len(company_df)), unsafe_allow_html=True)
    with c2: st.markdown(get_kpi_card_html("Repeat Recruiters", format_percentage(repeat_recruiter_rate(filtered_df))), unsafe_allow_html=True)
    with c3: st.markdown(get_kpi_card_html("Avg Offers/Recruiter", f"{company_df['total_offers'].mean():.1f}"), unsafe_allow_html=True)
    with c4: st.markdown(get_kpi_card_html("Offer Acceptance", format_percentage(offer_acceptance_rate(filtered_df))), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        top_hiring = company_df.nlargest(10, 'total_offers')
        fig1 = vis.bar_chart(top_hiring, x='company_name', y='total_offers', title="Top 10 Recruiters by Offers")
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Top 10 Recruiters by Offers: Companies ranked by total offers extended. High-volume recruiters are critical partners; losing them would significantly impact overall placement numbers. Dependency on a few recruiters is a strategic risk.")
    with col2:
        top_paying = company_df.nlargest(10, 'avg_package')
        fig2 = vis.bar_chart(top_paying, x='company_name', y='avg_package', title="Top 10 Recruiters by Avg Package (LPA)")
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Top 10 Recruiters by Avg Package: Companies ranked by mean salary offered. Premium recruiters attract top talent but may hire selectively. Compare this with the overall median to assess salary distribution quality.")
        
    col3, col4 = st.columns(2)
    with col3:
        # Repeat vs New
        repeat_cnt = company_df['is_repeat'].sum()
        new_cnt = len(company_df) - repeat_cnt
        fig3 = vis.donut_chart(['Repeat', 'New'], [repeat_cnt, new_cnt], title="Recruiter Loyalty (Repeat vs New)")
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Recruiter Loyalty: Proportion of companies that have recruited in multiple years (Repeat) vs. first-time visitors (New). A high repeat rate indicates strong institutional reputation; a high new rate suggests active outreach but uncertain retention.")
    with col4:
        # Pareto of offers
        fig4 = vis.pareto_chart(company_df.nlargest(20, 'total_offers'), 'company_name', 'total_offers', title="Recruiter Dependency Analysis")
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("Recruiter Dependency Analysis (Pareto): The bar shows individual company contributions to total offers; the orange line tracks cumulative percentage. If the top 5 recruiters account for >50% of offers, the placement cell faces concentration risk.")

    st.markdown("### Recruiter Summary Table")
    display_cols = {
        'company_name': 'Company',
        'sector': 'Sector',
        'company_type': 'Type',
        'total_offers': 'Offers',
        'accepted_offers': 'Accepted',
        'joined': 'Joined',
        'avg_package': 'Avg Package',
        'branches_hired': 'Branches Hired'
    }
    st.dataframe(
        company_df.sort_values('total_offers', ascending=False)[display_cols.keys()].rename(columns=display_cols).style.format({
            'Avg Package': '{:.2f}'
        }),
        use_container_width=True, hide_index=True
    )
else:
    st.info("No recruiters found for the selected filters.")
