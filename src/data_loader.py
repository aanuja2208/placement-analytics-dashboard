import streamlit as st
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'placement_data.csv')

@st.cache_data(ttl=300)
def load_data():
    """Load placement data from CSV with caching."""
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
        
    df = pd.read_csv(DATA_PATH)
    # Ensure proper dtypes
    df['graduation_year'] = df['graduation_year'].astype(int)
    df['cgpa'] = df['cgpa'].astype(float)
    df['package_lpa'] = pd.to_numeric(df['package_lpa'], errors='coerce').fillna(0.0)
    df['internships'] = df['internships'].astype(int)
    df['research_papers'] = df['research_papers'].astype(int)
    
    # Boolean-like columns
    bool_cols = ['offer_received', 'offer_accepted', 'joined_company', 
                 'internship_converted_to_ppo', 'eligible_for_placements',
                 'registered_for_placements', 'shortlisted', 'appeared_for_test',
                 'cleared_test', 'interviewed', 'is_repeat_recruiter']
                 
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0, 1: 1, 0: 0, '1.0': 1, '0.0': 0}).fillna(0).astype(int)
            
    return df

def apply_sidebar_filters(df, page_key='default'):
    """Apply common sidebar filters. Returns filtered dataframe.
    page_key ensures widgets have unique keys across pages."""
    if df.empty:
        return df
        
    st.sidebar.markdown('---')
    st.sidebar.markdown('### Filters')
    
    years = sorted(df['graduation_year'].unique())
    selected_years = st.sidebar.multiselect(
        'Graduation Year', years, default=years, key=f'{page_key}_year'
    )
    
    branches = sorted(df['branch'].unique())
    selected_branches = st.sidebar.multiselect(
        'Branch', branches, default=branches, key=f'{page_key}_branch'
    )
    
    outcomes = sorted(df['outcome'].unique())
    selected_outcomes = st.sidebar.multiselect(
        'Outcome', outcomes, default=outcomes, key=f'{page_key}_outcome'
    )
    
    if not selected_years or not selected_branches or not selected_outcomes:
        return df.iloc[0:0] # Return empty df with same columns
        
    mask = (
        df['graduation_year'].isin(selected_years) &
        df['branch'].isin(selected_branches) &
        df['outcome'].isin(selected_outcomes)
    )
    return df[mask].copy()

def validate_data(df):
    """Validate that required columns exist."""
    required = ['student_id', 'graduation_year', 'branch', 'cgpa', 'outcome']
    missing = [c for c in required if c not in df.columns]
    return len(missing) == 0, missing
