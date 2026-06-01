import pandas as pd
import numpy as np

def load_data():
    """Load student and yearly aggregated data"""
    try:
        df_students = pd.read_csv('data/students.csv')
        df_yearly = pd.read_csv('data/yearly_outcomes.csv')
        return df_students, df_yearly
    except FileNotFoundError:
        print("Error: Data files not found. Please run generate_sample_data.py first.")
        return None, None

def get_summary_stats(df_students):
    """Get overall summary statistics"""
    total_students = len(df_students)
    placed = df_students['placed_flag'].sum()
    higher_studies = df_students['higher_studies_flag'].sum()
    unplaced = df_students['unplaced_flag'].sum()
    
    return {
        'total_students': total_students,
        'placed_count': int(placed),
        'placed_pct': round(placed / total_students * 100, 1),
        'higher_studies_count': int(higher_studies),
        'higher_studies_pct': round(higher_studies / total_students * 100, 1),
        'unplaced_count': int(unplaced),
        'unplaced_pct': round(unplaced / total_students * 100, 1),
        'avg_cgpa': round(df_students['cgpa'].mean(), 2),
        'avg_internships': round(df_students['internships_count'].mean(), 2)
    }

def get_branch_analysis(df_students):
    """Get placement analysis by branch"""
    branch_stats = []
    
    for branch in df_students['branch'].unique():
        branch_data = df_students[df_students['branch'] == branch]
        total = len(branch_data)
        placed = branch_data['placed_flag'].sum()
        
        branch_stats.append({
            'branch': branch,
            'total_students': total,
            'placed': int(placed),
            'placement_rate': round(placed / total * 100, 1) if total > 0 else 0,
            'avg_cgpa': round(branch_data['cgpa'].mean(), 2),
            'avg_internships': round(branch_data['internships_count'].mean(), 2)
        })
    
    return pd.DataFrame(branch_stats).sort_values('placement_rate', ascending=False)

def get_cgpa_analysis(df_students):
    """Analyze placement by CGPA bands"""
    df_students['cgpa_band'] = pd.cut(df_students['cgpa'], 
                                       bins=[0, 6, 7, 8, 9, 10],
                                       labels=['<6', '6-7', '7-8', '8-9', '9-10'])
    
    cgpa_stats = []
    for band in ['<6', '6-7', '7-8', '8-9', '9-10']:
        band_data = df_students[df_students['cgpa_band'] == band]
        if len(band_data) > 0:
            placed = band_data['placed_flag'].sum()
            cgpa_stats.append({
                'cgpa_band': band,
                'total_students': len(band_data),
                'placed': int(placed),
                'placement_rate': round(placed / len(band_data) * 100, 1),
                'higher_studies': int(band_data['higher_studies_flag'].sum()),
                'unplaced': int(band_data['unplaced_flag'].sum())
            })
    
    return pd.DataFrame(cgpa_stats)

def get_internship_analysis(df_students):
    """Analyze placement by internship count"""
    internship_stats = []
    
    for internships in sorted(df_students['internships_count'].unique()):
        int_data = df_students[df_students['internships_count'] == internships]
        placed = int_data['placed_flag'].sum()
        
        internship_stats.append({
            'internships': int(internships),
            'total_students': len(int_data),
            'placed': int(placed),
            'placement_rate': round(placed / len(int_data) * 100, 1) if len(int_data) > 0 else 0,
            'higher_studies': int(int_data['higher_studies_flag'].sum()),
            'unplaced': int(int_data['unplaced_flag'].sum())
        })
    
    return pd.DataFrame(internship_stats)

def get_yearly_trends(df_yearly):
    """Return yearly trends for visualization"""
    return df_yearly[['graduation_year', 'placement_rate_pct', 
                       'higher_studies_rate_pct', 'unplaced_rate_pct',
                       'median_package_lpa', 'average_package_lpa']].copy()
