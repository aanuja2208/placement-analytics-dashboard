import pandas as pd
import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def generate_excel(df, summary_stats=None):
    output = io.BytesIO()
    try:
        import xlsxwriter
        engine = 'xlsxwriter'
    except ImportError:
        engine = 'openpyxl'
        
    with pd.ExcelWriter(output, engine=engine) as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
        
        if summary_stats:
            stats_df = pd.DataFrame(list(summary_stats.items()), columns=['Metric', 'Value'])
            stats_df['Metric'] = stats_df['Metric'].str.replace('_', ' ').str.title()
            stats_df.to_excel(writer, sheet_name='Executive Summary', index=False)
        
        # Branch-wise summary sheet
        if 'branch' in df.columns and 'outcome' in df.columns:
            branch_agg = df.groupby('branch').agg(
                Total_Students=('student_id', 'count'),
                Placed=('outcome', lambda x: (x == 'Placed').sum()),
                Higher_Studies=('outcome', lambda x: (x == 'Higher Studies').sum()),
                Unplaced=('outcome', lambda x: (x == 'Unplaced').sum()),
            ).reset_index()
            branch_agg['Placement_Rate_%'] = (branch_agg['Placed'] / branch_agg['Total_Students'] * 100).round(1)
            placed_pkg = df[df['outcome'] == 'Placed'].groupby('branch')['package_lpa'].agg(['mean', 'median']).round(2).reset_index()
            placed_pkg.columns = ['branch', 'Avg_Package_LPA', 'Median_Package_LPA']
            branch_summary = branch_agg.merge(placed_pkg, on='branch', how='left').fillna(0)
            branch_summary.to_excel(writer, sheet_name='Branch Summary', index=False)
        
        # Yearly trend sheet
        if 'graduation_year' in df.columns and 'outcome' in df.columns:
            yearly_agg = df.groupby('graduation_year').agg(
                Total=('student_id', 'count'),
                Placed=('outcome', lambda x: (x == 'Placed').sum()),
            ).reset_index()
            yearly_agg['Placement_Rate_%'] = (yearly_agg['Placed'] / yearly_agg['Total'] * 100).round(1)
            yearly_pkg = df[df['outcome'] == 'Placed'].groupby('graduation_year')['package_lpa'].agg(['mean', 'median']).round(2).reset_index()
            yearly_pkg.columns = ['graduation_year', 'Avg_Package_LPA', 'Median_Package_LPA']
            yearly_summary = yearly_agg.merge(yearly_pkg, on='graduation_year', how='left').fillna(0)
            yearly_summary.to_excel(writer, sheet_name='Yearly Trends', index=False)
            
        # Formatting headers if xlsxwriter available
        if engine == 'xlsxwriter':
            workbook = writer.book
            header_format = workbook.add_format({'bold': True, 'bg_color': '#1B2A4A', 'font_color': 'white', 'border': 1})
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_column('A:Z', 18)
                
    return output.getvalue()

def generate_pdf(df, title="Placement Report", summary_stats=None):
    from datetime import datetime
    import numpy as np
    
    output = io.BytesIO()
    from reportlab.lib.pagesizes import landscape, letter
    doc = SimpleDocTemplate(output, pagesize=landscape(letter),
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=30)
    
    styles = getSampleStyleSheet()
    
    title_style = styles['Title']
    title_style.textColor = colors.HexColor('#1B2A4A')
    
    subtitle_style = styles['Heading2']
    subtitle_style.textColor = colors.HexColor('#2E86AB')
    subtitle_style.spaceAfter = 10
    
    normal_style = styles['Normal']
    note_style = styles['Italic']
    note_style.textColor = colors.HexColor('#555555')
    note_style.fontSize = 9
    
    elements = []
    
    # -- Header --
    elements.append(Paragraph("Campus Placement Analytics System", title_style))
    elements.append(Paragraph(title, styles['Heading1']))
    date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    total_records = len(df) if df is not None and not df.empty else 0
    elements.append(Paragraph(f"Generated on: {date_str}  |  Total Records: {total_records}", normal_style))
    elements.append(Spacer(1, 15))
    
    # -- 1. Executive Summary KPIs --
    if summary_stats:
        elements.append(Paragraph("Executive Summary", subtitle_style))
        elements.append(Paragraph("Key performance indicators aggregated across all filtered data.", note_style))
        elements.append(Spacer(1, 6))
        data = [["Key Metric", "Value", "Description"]]
        metric_descriptions = {
            'total_students': 'Total number of students in the selected dataset',
            'placement_rate': 'Percentage of students who received and accepted a placement offer',
            'higher_studies_rate': 'Percentage of students who opted for higher education',
            'unplaced_rate': 'Percentage of students who remain unplaced',
            'avg_package': 'Mean salary package (LPA) offered to placed students',
            'median_package': 'Median salary package (LPA) - robust to outliers',
            'highest_package': 'Maximum salary package (LPA) offered in the dataset',
            'num_recruiters': 'Count of unique companies that made offers',
            'offer_acceptance_rate': 'Percentage of offers that were accepted by students',
        }
        for k, v in summary_stats.items():
            formatted_k = str(k).replace('_', ' ').title()
            formatted_v = f"{v:.2f}" if isinstance(v, float) else str(v)
            desc = metric_descriptions.get(k, '')
            data.append([formatted_k, formatted_v, desc])
            
        t = Table(data, colWidths=[180, 100, 320])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B2A4A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F8')])
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))
        
    if df is not None and not df.empty:
        # -- 2. Contextual Statistics --
        if "Department" in title and 'branch' in df.columns:
            elements.append(Paragraph("Department-wise Placement Breakdown", subtitle_style))
            elements.append(Paragraph("Aggregated statistics per branch/department, showing placement effectiveness and salary quality.", note_style))
            elements.append(Spacer(1, 6))
            branch_stats = df.groupby('branch').agg(
                Total=('student_id', 'count'),
                Placed=('outcome', lambda x: (x == 'Placed').sum()),
                HigherStudies=('outcome', lambda x: (x == 'Higher Studies').sum()),
                Avg_Package=('package_lpa', lambda x: x[df.loc[x.index, 'outcome'] == 'Placed'].mean()),
                Median_Package=('package_lpa', lambda x: x[df.loc[x.index, 'outcome'] == 'Placed'].median()),
            ).fillna(0).reset_index()
            
            branch_stats['Placement_Rate'] = (branch_stats['Placed'] / branch_stats['Total'] * 100).round(1)
            branch_stats['Unplaced'] = branch_stats['Total'] - branch_stats['Placed'] - branch_stats['HigherStudies']
            
            b_data = [["Branch", "Total", "Placed", "Higher Studies", "Unplaced", "Rate (%)", "Avg Pkg", "Med Pkg"]]
            for _, row in branch_stats.iterrows():
                b_data.append([
                    str(row['branch']), str(int(row['Total'])), str(int(row['Placed'])),
                    str(int(row['HigherStudies'])), str(int(row['Unplaced'])),
                    f"{row['Placement_Rate']:.1f}", f"{row['Avg_Package']:.2f}", f"{row['Median_Package']:.2f}"
                ])
                
            bt = Table(b_data, colWidths=[70, 60, 60, 80, 70, 60, 70, 70])
            bt.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#22A06B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F8')])
            ]))
            elements.append(bt)
            elements.append(Spacer(1, 20))
            
        elif "Recruiter" in title and 'company_name' in df.columns:
            elements.append(Paragraph("Top 15 Recruiters by Hiring Volume", subtitle_style))
            elements.append(Paragraph("Companies ranked by total placements made. High-volume recruiters are critical strategic partners.", note_style))
            elements.append(Spacer(1, 6))
            rec_stats = df[df['company_name'] != ""].groupby('company_name').agg(
                Offers=('student_id', 'count'),
                Avg_Package=('package_lpa', 'mean'),
                Median_Package=('package_lpa', 'median'),
                Sector=('sector', 'first'),
                Type=('company_type', 'first'),
            ).nlargest(15, 'Offers').reset_index()
            
            r_data = [["Company", "Type", "Sector", "Offers", "Avg Pkg", "Med Pkg"]]
            for _, row in rec_stats.iterrows():
                r_data.append([
                    str(row['company_name'])[:20], str(row['Type']), str(row['Sector']),
                    str(row['Offers']), f"{row['Avg_Package']:.2f}", f"{row['Median_Package']:.2f}"
                ])
                
            rt = Table(r_data, colWidths=[130, 80, 90, 60, 70, 70])
            rt.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F18F01')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F8')])
            ]))
            elements.append(rt)
            elements.append(Spacer(1, 20))
            
        elif "Salary" in title and 'package_lpa' in df.columns:
            elements.append(Paragraph("Salary Distribution Analysis", subtitle_style))
            elements.append(Paragraph("Statistical summary of compensation packages offered to placed students.", note_style))
            elements.append(Spacer(1, 6))
            
            stats = df['package_lpa'].describe()
            iqr = stats['75%'] - stats['25%']
            
            s_data = [
                ["Statistic", "Value (LPA)", "Interpretation"],
                ["Mean", f"{stats['mean']:.2f}", "Average salary; sensitive to outlier offers"],
                ["Median", f"{stats['50%']:.2f}", "Middle value; robust measure of typical salary"],
                ["Std Dev", f"{stats['std']:.2f}", "Spread of salary distribution"],
                ["Min", f"{stats['min']:.2f}", "Lowest package offered"],
                ["25th Percentile", f"{stats['25%']:.2f}", "Bottom quartile boundary"],
                ["75th Percentile", f"{stats['75%']:.2f}", "Top quartile boundary"],
                ["Max", f"{stats['max']:.2f}", "Highest package offered"],
                ["IQR", f"{iqr:.2f}", "Interquartile range; core salary spread"],
            ]
            
            st_table = Table(s_data, colWidths=[130, 100, 300])
            st_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6554C0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F8')])
            ]))
            elements.append(st_table)
            elements.append(Spacer(1, 15))
            
            # Salary by company type
            if 'company_type' in df.columns:
                elements.append(Paragraph("Package by Company Type", subtitle_style))
                type_stats = df.groupby('company_type')['package_lpa'].agg(['count', 'mean', 'median', 'min', 'max']).round(2).reset_index()
                type_stats.columns = ['Company Type', 'Count', 'Mean', 'Median', 'Min', 'Max']
                ct_data = [type_stats.columns.tolist()]
                for _, row in type_stats.iterrows():
                    ct_data.append([str(row['Company Type']), str(int(row['Count'])), f"{row['Mean']:.2f}", f"{row['Median']:.2f}", f"{row['Min']:.2f}", f"{row['Max']:.2f}"])
                ct_table = Table(ct_data, colWidths=[110, 60, 80, 80, 80, 80])
                ct_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F8')])
                ]))
                elements.append(ct_table)
                elements.append(Spacer(1, 20))
        
        elif "Executive" in title:
            # Yearly trend table for executive summary
            if 'graduation_year' in df.columns:
                elements.append(Paragraph("Year-over-Year Performance", subtitle_style))
                elements.append(Paragraph("Annual placement metrics showing institutional trajectory over time.", note_style))
                elements.append(Spacer(1, 6))
                yearly = df.groupby('graduation_year').agg(
                    Total=('student_id', 'count'),
                    Placed=('outcome', lambda x: (x == 'Placed').sum()),
                ).reset_index()
                yearly['Rate_%'] = (yearly['Placed'] / yearly['Total'] * 100).round(1)
                placed_pkg = df[df['outcome'] == 'Placed'].groupby('graduation_year')['package_lpa'].agg(['mean', 'median']).round(2).reset_index()
                placed_pkg.columns = ['graduation_year', 'Avg_Pkg', 'Med_Pkg']
                yearly = yearly.merge(placed_pkg, on='graduation_year', how='left').fillna(0)
                
                y_data = [["Year", "Total", "Placed", "Rate (%)", "Avg Pkg (LPA)", "Med Pkg (LPA)"]]
                for _, row in yearly.iterrows():
                    y_data.append([
                        str(int(row['graduation_year'])), str(int(row['Total'])), str(int(row['Placed'])),
                        f"{row['Rate_%']:.1f}", f"{row['Avg_Pkg']:.2f}", f"{row['Med_Pkg']:.2f}"
                    ])
                yt = Table(y_data, colWidths=[80, 70, 70, 80, 100, 100])
                yt.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B2A4A')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F8')])
                ]))
                elements.append(yt)
                elements.append(Spacer(1, 20))
            
        # -- 3. Data Sample --
        elements.append(Paragraph(f"Detailed Data Sample (Top 50 of {len(df)} Records)", subtitle_style))
        elements.append(Paragraph("A representative sample of individual student records from the filtered dataset.", note_style))
        elements.append(Spacer(1, 6))
        display_df = df.head(50)
        
        important_cols = ['student_id', 'branch', 'graduation_year', 'cgpa', 'outcome', 'company_name', 'package_lpa']
        cols = [c for c in important_cols if c in display_df.columns]
        if not cols:
            cols = display_df.columns.tolist()[:7]
            
        headers = [c.replace('_', ' ').title() for c in cols]
        table_data = [headers]
        
        for _, row in display_df.iterrows():
            row_data = []
            for c in cols:
                val = row[c]
                if isinstance(val, float):
                    row_data.append(f"{val:.2f}")
                else:
                    row_data.append(str(val)[:20] if val != "" else "-")
            table_data.append(row_data)
            
        t_data = Table(table_data, repeatRows=1)
        t_data.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DEE2E6')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F8')])
        ]))
        elements.append(t_data)
        
    doc.build(elements)
    return output.getvalue()

