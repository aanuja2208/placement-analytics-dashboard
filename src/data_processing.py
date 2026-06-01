import pandas as pd
import numpy as np

def add_derived_columns(df):
    """Add derived columns to the dataframe."""
    df = df.copy()
    if 'outcome' in df.columns:
        df['placed_flag'] = (df['outcome'] == 'Placed').astype(int)
        df['higher_studies_flag'] = (df['outcome'] == 'Higher Studies').astype(int)
        df['unplaced_flag'] = (df['outcome'] == 'Unplaced').astype(int)
    
    if 'cgpa' in df.columns:
        df['cgpa_band'] = pd.cut(df['cgpa'], 
                               bins=[0, 6, 7, 8, 9, 10], 
                               labels=['<6', '6-7', '7-8', '8-9', '9+'],
                               right=False)
                               
    if 'package_lpa' in df.columns and 'outcome' in df.columns:
        placed = df['outcome'] == 'Placed'
        df['package_band'] = pd.cut(df.loc[placed, 'package_lpa'], 
                                  bins=[0, 5, 8, 12, 18, 100], 
                                  labels=['<5', '5-8', '8-12', '12-18', '18+'],
                                  right=False)
        # Add 'N/A' for non-placed
        df['package_band'] = df['package_band'].cat.add_categories('N/A').fillna('N/A')
    
    return df

def get_yearly_summary(df):
    if df.empty:
        return pd.DataFrame()
        
    df = add_derived_columns(df)
    
    summary = df.groupby('graduation_year').agg(
        total_students=('student_id', 'count'),
        placed=('placed_flag', 'sum'),
        higher_studies=('higher_studies_flag', 'sum'),
        unplaced=('unplaced_flag', 'sum'),
        avg_package=('package_lpa', lambda x: x[df.loc[x.index, 'outcome'] == 'Placed'].mean()),
        median_package=('package_lpa', lambda x: x[df.loc[x.index, 'outcome'] == 'Placed'].median()),
        num_recruiters=('company_name', lambda x: x[x != ""].nunique()),
        num_offers=('offer_received', 'sum')
    ).reset_index()
    
    summary['placement_rate'] = (summary['placed'] / summary['total_students'] * 100).fillna(0)
    summary['higher_studies_rate'] = (summary['higher_studies'] / summary['total_students'] * 100).fillna(0)
    summary['unplaced_rate'] = (summary['unplaced'] / summary['total_students'] * 100).fillna(0)
    
    # Offer acceptance rate
    offers_received = df.groupby('graduation_year')['offer_received'].sum()
    offers_accepted = df.groupby('graduation_year')['offer_accepted'].sum()
    rates = offers_accepted.values / np.where(offers_received.values > 0, offers_received.values, 1) * 100
    summary['offer_acceptance_rate'] = pd.Series(rates, index=summary.index).fillna(0)
    
    summary = summary.fillna(0)
    return summary.rename(columns={'graduation_year': 'year'})

def get_branch_summary(df):
    if df.empty:
        return pd.DataFrame()
        
    df = add_derived_columns(df)
    
    summary = df.groupby('branch').agg(
        total_students=('student_id', 'count'),
        placed=('placed_flag', 'sum'),
        higher_studies=('higher_studies_flag', 'sum'),
        unplaced=('unplaced_flag', 'sum'),
        avg_package=('package_lpa', lambda x: x[df.loc[x.index, 'outcome'] == 'Placed'].mean()),
        median_package=('package_lpa', lambda x: x[df.loc[x.index, 'outcome'] == 'Placed'].median()),
        avg_cgpa=('cgpa', 'mean'),
        avg_internships=('internships', 'mean'),
        num_recruiters=('company_name', lambda x: x[x != ""].nunique())
    ).reset_index()
    
    summary['placement_rate'] = (summary['placed'] / summary['total_students'] * 100).fillna(0)
    summary['higher_studies_rate'] = (summary['higher_studies'] / summary['total_students'] * 100).fillna(0)
    summary['unplaced_rate'] = (summary['unplaced'] / summary['total_students'] * 100).fillna(0)
    
    summary = summary.fillna(0)
    return summary

def get_company_summary(df):
    if df.empty:
        return pd.DataFrame()
        
    df_placed = df[df['company_name'] != ""]
    if df_placed.empty:
        return pd.DataFrame()
        
    summary = df_placed.groupby('company_name').agg(
        sector=('sector', 'first'),
        company_type=('company_type', 'first'),
        total_offers=('offer_received', 'sum'),
        accepted_offers=('offer_accepted', 'sum'),
        joined=('joined_company', 'sum'),
        avg_package=('package_lpa', 'mean'),
        median_package=('package_lpa', 'median'),
        branches_hired=('branch', lambda x: ", ".join(sorted(x.unique()))),
        is_repeat=('is_repeat_recruiter', 'max') # 1 if repeat, 0 if not
    ).reset_index()
    
    return summary.fillna(0)

def get_sector_summary(df):
    if df.empty:
        return pd.DataFrame()
        
    df_placed = df[df['sector'] != ""]
    if df_placed.empty:
        return pd.DataFrame()
        
    summary = df_placed.groupby('sector').agg(
        total_offers=('offer_received', 'sum'),
        accepted_offers=('offer_accepted', 'sum'),
        avg_package=('package_lpa', 'mean'),
        median_package=('package_lpa', 'median'),
        num_recruiters=('company_name', 'nunique')
    ).reset_index()
    
    return summary.fillna(0)

def get_cgpa_band_summary(df):
    if df.empty:
        return pd.DataFrame()
        
    df = add_derived_columns(df)
    
    summary = df.groupby('cgpa_band', observed=False).agg(
        total_students=('student_id', 'count'),
        placed=('placed_flag', 'sum'),
        higher_studies=('higher_studies_flag', 'sum'),
        unplaced=('unplaced_flag', 'sum')
    ).reset_index()
    
    summary['placement_rate'] = (summary['placed'] / summary['total_students'] * 100).fillna(0)
    
    numeric_cols = summary.select_dtypes(include=[np.number]).columns
    summary[numeric_cols] = summary[numeric_cols].fillna(0)
    return summary

def get_internship_summary(df):
    if df.empty:
        return pd.DataFrame()
        
    df = add_derived_columns(df)
    
    summary = df.groupby('internships').agg(
        total_students=('student_id', 'count'),
        placed=('placed_flag', 'sum'),
        higher_studies=('higher_studies_flag', 'sum'),
        unplaced=('unplaced_flag', 'sum')
    ).reset_index()
    
    summary['placement_rate'] = (summary['placed'] / summary['total_students'] * 100).fillna(0)
    
    numeric_cols = summary.select_dtypes(include=[np.number]).columns
    summary[numeric_cols] = summary[numeric_cols].fillna(0)
    return summary

def get_funnel_data(df):
    if df.empty:
        return pd.DataFrame()
        
    total = len(df)
    eligible = df['eligible_for_placements'].sum()
    registered = df['registered_for_placements'].sum()
    shortlisted = df['shortlisted'].sum()
    appeared = df['appeared_for_test'].sum()
    cleared = df['cleared_test'].sum()
    interviewed = df['interviewed'].sum()
    received = df['offer_received'].sum()
    accepted = df['offer_accepted'].sum()
    joined = df['joined_company'].sum()
    
    stages = [
        'Total Students', 'Eligible', 'Registered', 'Shortlisted',
        'Appeared for Test', 'Cleared Test', 'Interviewed',
        'Offer Received', 'Offer Accepted', 'Joined'
    ]
    
    counts = [
        total, eligible, registered, shortlisted,
        appeared, cleared, interviewed,
        received, accepted, joined
    ]
    
    percentages = [(c / total * 100) if total > 0 else 0 for c in counts]
    
    return pd.DataFrame({
        'stage': stages,
        'count': counts,
        'percentage': percentages
    })

def get_cohort_summary(df, group_cols):
    if df.empty:
        return pd.DataFrame()
        
    df = add_derived_columns(df)
    
    summary = df.groupby(group_cols).agg(
        total_students=('student_id', 'count'),
        placed=('placed_flag', 'sum'),
        higher_studies=('higher_studies_flag', 'sum'),
        unplaced=('unplaced_flag', 'sum'),
        avg_package=('package_lpa', lambda x: x[df.loc[x.index, 'outcome'] == 'Placed'].mean()),
        median_package=('package_lpa', lambda x: x[df.loc[x.index, 'outcome'] == 'Placed'].median()),
        avg_internships=('internships', 'mean')
    ).reset_index()
    
    summary['placement_rate'] = (summary['placed'] / summary['total_students'] * 100).fillna(0)
    summary['higher_studies_rate'] = (summary['higher_studies'] / summary['total_students'] * 100).fillna(0)
    summary['unplaced_rate'] = (summary['unplaced'] / summary['total_students'] * 100).fillna(0)
    
    return summary.fillna(0)

def get_correlation_matrix(df):
    if df.empty:
        return pd.DataFrame()
        
    df = add_derived_columns(df)
    
    cols = ['cgpa', 'class_10_percent', 'class_12_percent', 'internships', 'research_papers', 'placed_flag']
    available_cols = [c for c in cols if c in df.columns]
    
    if not available_cols:
        return pd.DataFrame()
        
    return df[available_cols].corr().fillna(0)
