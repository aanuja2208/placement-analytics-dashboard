import streamlit as st
import pandas as pd
from src.data_loader import load_data, apply_sidebar_filters
from src.data_processing import get_yearly_summary
from src.forecasting import forecast_all_metrics, get_historical_and_forecast
from src.utils import get_kpi_card_html
import src.visualizations as vis

st.set_page_config(page_title="Forecasting", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

# No sidebar filters on forecasting usually, as it needs all historical data
st.sidebar.markdown("### Settings")
years_ahead = st.sidebar.slider("Forecast Years", 1, 5, 3)
method = st.sidebar.selectbox("Forecasting Method", ["moving_average", "exponential_smoothing"])

st.title("Demand & Performance Forecasting")
st.markdown("Predict future placement trends based on historical data.")

yearly_df = get_yearly_summary(df)

if not yearly_df.empty:
    forecasts = forecast_all_metrics(yearly_df, years_ahead=years_ahead, method=method)
    
    # KPI Cards for next year
    st.markdown("### Next Year Predictions")
    cols = st.columns(4)
    idx = 0
    for metric_name, data in forecasts.items():
        if idx >= 4: break
        next_yr_val = data['forecast']['forecast'].iloc[0]
        
        # Determine delta color meaning
        delta_color = 'success' if data['risk'] == 'Improving' else ('danger' if data['risk'] == 'Declining' else 'normal')
        if "Unplaced" in metric_name:
            delta_color = 'success' if data['risk'] == 'Declining' else ('danger' if data['risk'] == 'Improving' else 'normal')
            
        html = get_kpi_card_html(metric_name, f"{next_yr_val:.1f}", data['risk'], delta_color)
        cols[idx].markdown(html, unsafe_allow_html=True)
        idx += 1
        
    st.markdown("---")
    
    # Charts
    c1, c2 = st.columns(2)
    
    hist_pl, for_pl = get_historical_and_forecast(yearly_df, 'placement_rate', years_ahead, method)
    if not hist_pl.empty:
        with c1:
            fig1 = vis.forecast_line(hist_pl, for_pl, x='year', y='value', title="Placement Rate Forecast (%)")
            st.plotly_chart(fig1, use_container_width=True)
            st.caption("Placement Rate Forecast: Solid line shows historical rates; dashed line shows projected rates using the selected forecasting method. Moving average smooths short-term noise; exponential smoothing weights recent years more heavily. The damped trend prevents unrealistic extrapolation.")
            
    hist_med, for_med = get_historical_and_forecast(yearly_df, 'median_package', years_ahead, method)
    if not hist_med.empty:
        with c2:
            fig2 = vis.forecast_line(hist_med, for_med, x='year', y='value', title="Median Package Forecast (LPA)")
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("Median Package Forecast: Projects future salary levels based on historical trends. A consistent upward forecast suggests sustained recruiter demand and improving market conditions for graduates.")

    c3, c4 = st.columns(2)
    
    hist_rec, for_rec = get_historical_and_forecast(yearly_df, 'num_recruiters', years_ahead, method)
    if not hist_rec.empty:
        with c3:
            fig3 = vis.forecast_line(hist_rec, for_rec, x='year', y='value', title="Recruiter Demand Forecast")
            st.plotly_chart(fig3, use_container_width=True)
            st.caption("Recruiter Demand Forecast: Predicts the number of companies expected to participate in campus placements. A declining forecast may signal the need for proactive industry outreach by the placement cell.")
            
    hist_up, for_up = get_historical_and_forecast(yearly_df, 'unplaced_rate', years_ahead, method)
    if not hist_up.empty:
        with c4:
            fig4 = vis.forecast_line(hist_up, for_up, x='year', y='value', title="Unplaced Rate Forecast (%)")
            st.plotly_chart(fig4, use_container_width=True)
            st.caption("Unplaced Rate Forecast: Projects the percentage of students likely to remain unplaced. For this metric, a declining trend is desirable. Rising forecasts should trigger early interventions such as skill workshops or additional recruitment drives.")
