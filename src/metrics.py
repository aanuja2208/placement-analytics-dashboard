import pandas as pd
import numpy as np

def placement_rate(df):
    if df.empty: return 0.0
    return float(len(df[df['outcome'] == 'Placed']) / len(df) * 100)

def higher_studies_rate(df):
    if df.empty: return 0.0
    return float(len(df[df['outcome'] == 'Higher Studies']) / len(df) * 100)

def unplaced_rate(df):
    if df.empty: return 0.0
    return float(len(df[df['outcome'] == 'Unplaced']) / len(df) * 100)

def offer_acceptance_rate(df):
    if df.empty: return 0.0
    received = df['offer_received'].sum()
    if received == 0: return 0.0
    return float(df['offer_accepted'].sum() / received * 100)

def repeat_recruiter_rate(df):
    if df.empty: return 0.0
    df_placed = df[df['company_name'] != ""]
    if df_placed.empty: return 0.0
    companies = df_placed.groupby('company_name')['is_repeat_recruiter'].max()
    if len(companies) == 0: return 0.0
    return float(companies.sum() / len(companies) * 100)

def internship_conversion_rate(df):
    if df.empty: return 0.0
    with_internships = df[df['internships'] > 0]
    if with_internships.empty: return 0.0
    return float(with_internships['internship_converted_to_ppo'].sum() / len(with_internships) * 100)

def joining_conversion_rate(df):
    if df.empty: return 0.0
    accepted = df['offer_accepted'].sum()
    if accepted == 0: return 0.0
    return float(df['joined_company'].sum() / accepted * 100)

def recruiter_dependency(df, top_n=5):
    if df.empty: return 0.0
    df_placed = df[df['company_name'] != ""]
    if df_placed.empty: return 0.0
    total_offers = df_placed['offer_received'].sum()
    if total_offers == 0: return 0.0
    top_offers = df_placed.groupby('company_name')['offer_received'].sum().nlargest(top_n).sum()
    return float(top_offers / total_offers * 100)

def branch_opportunity_index(branch_df, weights=None):
    if branch_df.empty: return 0.0
    if weights is None:
        weights = {
            'placement_rate': 0.25,
            'median_package': 0.20,
            'recruiter_count': 0.15,
            'recruiter_diversity': 0.10,
            'higher_studies_rate': 0.10,
            'internship_conversion': 0.10,
            'growth': 0.05,
            'unplaced_penalty': -0.05
        }
        
    placement = placement_rate(branch_df)
    placed_df = branch_df[branch_df['outcome'] == 'Placed']
    med_pkg = placed_df['package_lpa'].median() if not placed_df.empty else 0
    recruiter_cnt = placed_df['company_name'].nunique()
    
    # Normalize components (simple 0-100 scaling, assuming max reasonable values)
    # This is a basic implementation, can be refined based on actual max values
    norm_placement = placement
    norm_pkg = min(med_pkg / 25.0 * 100, 100) # Assuming 25LPA is "100%"
    norm_recruiters = min(recruiter_cnt / 30.0 * 100, 100) # Assuming 30 companies is "100%"
    
    sectors = placed_df['sector'].nunique()
    norm_diversity = min(sectors / 6.0 * 100, 100) # 6 sectors
    
    norm_higher = higher_studies_rate(branch_df)
    norm_internship = internship_conversion_rate(branch_df)
    
    # Simple growth proxy: assume 50 for now or calculate actual YoY
    norm_growth = 50.0 
    
    unplaced = unplaced_rate(branch_df)
    
    sum_weights = sum(val for key, val in weights.items() if key != 'unplaced_penalty')
    if sum_weights <= 0:
        sum_weights = 1.0
        
    penalty_weight = weights.get('unplaced_penalty', 0)
    if penalty_weight > 0:
        penalty_weight = -penalty_weight
        
    score = (
        norm_placement * weights.get('placement_rate', 0) +
        norm_pkg * weights.get('median_package', 0) +
        norm_recruiters * weights.get('recruiter_count', 0) +
        norm_diversity * weights.get('recruiter_diversity', 0) +
        norm_higher * weights.get('higher_studies_rate', 0) +
        norm_internship * weights.get('internship_conversion', 0) +
        norm_growth * weights.get('growth', 0) +
        unplaced * penalty_weight
    ) / sum_weights
    
    return float(max(0, min(100, score)))

def get_executive_kpis(df):
    if df.empty:
        return {}
        
    placed_df = df[df['outcome'] == 'Placed']
    
    return {
        'total_students': len(df),
        'placement_rate': placement_rate(df),
        'higher_studies_rate': higher_studies_rate(df),
        'unplaced_rate': unplaced_rate(df),
        'avg_package': placed_df['package_lpa'].mean() if not placed_df.empty else 0.0,
        'median_package': placed_df['package_lpa'].median() if not placed_df.empty else 0.0,
        'highest_package': placed_df['package_lpa'].max() if not placed_df.empty else 0.0,
        'num_recruiters': placed_df['company_name'].nunique() if not placed_df.empty else 0,
        'offer_acceptance_rate': offer_acceptance_rate(df)
    }
