import streamlit as st
import pandas as pd
from src.data_loader import load_data, apply_sidebar_filters
from src.report_generator import generate_csv, generate_excel, generate_pdf
from src.metrics import get_executive_kpis

st.set_page_config(page_title="Automated Reports", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

filtered_df = apply_sidebar_filters(df, page_key='reports')

st.title("Automated Report Generation")
st.markdown("Download professional reports for faculty, HODs, and administration.")
st.markdown('''
Generate downloadable reports in CSV, Excel, or PDF format. Each report type focuses on different aspects:
- **Executive Summary**: Full dataset with global KPIs and outcome metrics
- **Department-wise Placement**: Data sorted by branch and year for HOD-level review
- **Recruiter Performance**: Placed student data for analyzing company hiring patterns
- **Salary Distribution**: Placed students sorted by package for compensation analysis

PDF reports include contextual statistical tables (e.g., branch-wise breakdown, top recruiters) in addition to the raw data sample.
''')

col1, col2 = st.columns(2)
with col1:
    report_type = st.selectbox("Select Report Type", [
        "Executive Summary",
        "Department-wise Placement",
        "Recruiter Performance",
        "Salary Distribution"
    ])
    
with col2:
    export_format = st.selectbox("Export Format", ["CSV", "Excel", "PDF"])

if st.button("Generate Report", type="primary"):
    with st.spinner(f"Generating {report_type} in {export_format} format..."):
        # Select data based on report type
        if report_type == "Executive Summary":
            data_to_export = filtered_df
        elif report_type == "Department-wise Placement":
            data_to_export = filtered_df.sort_values(['branch', 'graduation_year'])
        elif report_type == "Recruiter Performance":
            data_to_export = filtered_df[filtered_df['outcome'] == 'Placed']
        else: # Salary Distribution
            data_to_export = filtered_df[filtered_df['outcome'] == 'Placed'].sort_values('package_lpa', ascending=False)
            
        summary_stats = get_executive_kpis(filtered_df)
        
        # Generate file
        file_data = None
        mime_type = ""
        file_ext = ""
        
        if export_format == "CSV":
            file_data = generate_csv(data_to_export)
            mime_type = "text/csv"
            file_ext = "csv"
        elif export_format == "Excel":
            file_data = generate_excel(data_to_export, summary_stats)
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            file_ext = "xlsx"
        elif export_format == "PDF":
            file_data = generate_pdf(data_to_export, title=f"{report_type} Report", summary_stats=summary_stats)
            mime_type = "application/pdf"
            file_ext = "pdf"
            
        file_name = f"{report_type.replace(' ', '_').lower()}_report.{file_ext}"
        
        st.success("Report generated successfully!")
        st.download_button(
            label=f"Download {file_name}",
            data=file_data,
            file_name=file_name,
            mime=mime_type,
            use_container_width=True
        )
