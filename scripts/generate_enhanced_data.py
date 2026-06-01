import pandas as pd
import numpy as np
import os
import random

# Configuration
TOTAL_STUDENTS_PER_YEAR = 1000
YEARS = list(range(2015, 2025)) # 10 years: 2015 to 2024 (10,000 students total)
BRANCHES = ['CSE', 'IT', 'ECE', 'EE', 'ME', 'CE', 'BT']

# Recruiter mapping
COMPANIES = {
    # Tier 1 Product (Elite, High package, low selection rate)
    'Google': ('product', 'tier_1', 'Tech'),
    'Microsoft': ('product', 'tier_1', 'Tech'),
    'Amazon': ('product', 'tier_1', 'Tech'),
    'Adobe': ('product', 'tier_1', 'Tech'),
    'NVIDIA': ('product', 'tier_1', 'Tech'),
    'Qualcomm': ('product', 'tier_1', 'Tech'),
    'Apple': ('product', 'tier_1', 'Tech'),
    
    # Tier 2 Product
    'Samsung': ('product', 'tier_2', 'Tech'),
    'Oracle': ('product', 'tier_2', 'Tech'),
    'Intel': ('product', 'tier_2', 'Tech'),
    'Cisco': ('product', 'tier_2', 'Tech'),
    'Salesforce': ('product', 'tier_2', 'Tech'),
    'VMware': ('product', 'tier_2', 'Tech'),
    
    # Startups (High variance, flexible)
    'Flipkart': ('startup', 'tier_2', 'Tech'),
    'Swiggy': ('startup', 'tier_2', 'Tech'),
    'Zomato': ('startup', 'tier_2', 'Tech'),
    'Razorpay': ('startup', 'tier_2', 'Tech'),
    'PhonePe': ('startup', 'tier_2', 'Tech'),
    'Ola': ('startup', 'tier_3', 'Tech'),
    'Paytm': ('startup', 'tier_3', 'Tech'),
    'Meesho': ('startup', 'tier_3', 'Tech'),

    # Consulting
    'McKinsey': ('consulting', 'tier_1', 'Consulting'),
    'BCG': ('consulting', 'tier_1', 'Consulting'),
    'Bain': ('consulting', 'tier_1', 'Consulting'),
    'Deloitte': ('consulting', 'tier_2', 'Consulting'),
    'EY': ('consulting', 'tier_2', 'Consulting'),
    'PwC': ('consulting', 'tier_2', 'Consulting'),
    'KPMG': ('consulting', 'tier_2', 'Consulting'),
    'Accenture': ('consulting', 'tier_3', 'Consulting'),

    # Core Engineering
    'L&T': ('core', 'tier_2', 'Core Engineering'),
    'Siemens': ('core', 'tier_2', 'Core Engineering'),
    'ABB': ('core', 'tier_2', 'Core Engineering'),
    'Bosch': ('core', 'tier_2', 'Core Engineering'),
    'Honeywell': ('core', 'tier_2', 'Core Engineering'),
    'Tata Steel': ('core', 'tier_2', 'Core Engineering'),
    'Reliance': ('core', 'tier_3', 'Core Engineering'),
    'GE': ('core', 'tier_2', 'Core Engineering'),

    # Service (Mass Recruiters - high volume, low packages)
    'TCS': ('service', 'tier_3', 'Tech'),
    'Infosys': ('service', 'tier_3', 'Tech'),
    'Wipro': ('service', 'tier_3', 'Tech'),
    'Cognizant': ('service', 'tier_3', 'Tech'),
    'Tech Mahindra': ('service', 'tier_3', 'Tech'),
    'Capgemini': ('service', 'tier_3', 'Tech'),
    'HCL': ('service', 'tier_3', 'Tech')
}

# Project Domains and Skills by branch group
BRANCH_DOMAINS = {
    'CSE_IT': ['Machine Learning', 'Web Development', 'Data Science', 'Cloud Computing', 'Cybersecurity', 'Blockchain', 'Mobile Apps'],
    'ECE_EE': ['IoT', 'Robotics', 'Embedded Systems', 'Hardware & VLSI', 'Power Systems', 'Signal Processing'],
    'ME_CE': ['AutoCAD Design', 'Solidworks Modeling', 'Structural Engineering', 'Project Management', 'Robotics'],
    'BT': ['Biotech Research', 'Bioinformatics', 'Data Analysis', 'Clinical Analytics']
}

BRANCH_SKILLS = {
    'CSE': ['Python', 'Java', 'C++', 'SQL', 'React', 'Node.js', 'Docker', 'AWS', 'TensorFlow'],
    'IT': ['JavaScript', 'Python', 'SQL', 'HTML/CSS', 'React', 'Node.js', 'Docker', 'AWS', 'Java'],
    'ECE': ['C++', 'MATLAB', 'VHDL', 'Python', 'Embedded Systems', 'IoT', 'SQL'],
    'EE': ['MATLAB', 'C++', 'IoT', 'Power Systems', 'Excel', 'Python', 'AutoCAD'],
    'ME': ['AutoCAD', 'Solidworks', 'Ansys', 'Excel', 'MATLAB', 'Python', 'Project Management'],
    'CE': ['AutoCAD', 'Revit', 'Project Management', 'Excel', 'STAAD Pro', 'Civil 3D'],
    'BT': ['Python', 'R', 'Excel', 'Data Analysis', 'Tableau', 'Bioinformatics', 'SQL']
}

def generate_skewed_package(company_type, company_tier, inflation_factor, covid_impact):
    """Generate realistically skewed salary package (LPA) using lognormal or beta distributions."""
    if company_type == 'product':
        if company_tier == 'tier_1':
            # 20 - 60 LPA (rare, highly right-skewed)
            base = 20.0 + np.random.lognormal(mean=1.8, sigma=0.5)
            package = np.clip(base, 20.0, 60.0)
        else:
            # Tier 2 Product: 10 - 25 LPA
            base = 10.0 + np.random.lognormal(mean=1.5, sigma=0.4)
            package = np.clip(base, 10.0, 25.0)
            
    elif company_type == 'startup':
        # Startups: 5 - 20 LPA (very high variance)
        base = 5.0 + np.random.lognormal(mean=1.6, sigma=0.6)
        package = np.clip(base, 5.0, 20.0)
        
    elif company_type == 'consulting':
        if company_tier == 'tier_1':
            # Tier 1 Consulting: 12 - 22 LPA
            package = np.random.normal(16.0, 2.0)
        else:
            # Tier 2/3 Consulting: 6 - 12 LPA
            package = np.random.normal(8.5, 1.5)
            
    elif company_type == 'core':
        # Core: 6 - 18 LPA
        package = np.random.normal(9.0, 2.5)
        package = np.clip(package, 6.0, 18.0)
        
    else: # service (mass recruiters)
        # Service: 3 - 8 LPA (heavily clustered around 3.5 - 4.5)
        package = np.random.normal(4.0, 0.8)
        package = np.clip(package, 3.0, 8.0)
        
    # Apply yearly inflation and covid adjustments
    package = package * inflation_factor * (1.0 - covid_impact * 0.10)
    return round(package, 2)

def generate_data():
    np.random.seed(42)
    random.seed(42)
    
    records = []
    total_generated = 0
    
    for year in YEARS:
        # Yearly trend parameters
        # Gradual package inflation
        inflation_factor = 1.0 + (year - 2015) * 0.045
        
        # Covid impact flags (2020 and 2021)
        is_covid_year = year in [2020, 2021]
        covid_hiring_drop = 0.20 if is_covid_year else 0.0
        covid_internship_drop = 0.30 if is_covid_year else 0.0
        
        # Post-covid startup boom (2022, 2023)
        is_post_covid_boom = year in [2022, 2023]
        startup_boom_factor = 1.35 if is_post_covid_boom else 1.0
        
        # 2024 Tech Correction
        is_correction_year = (year == 2024)
        correction_drop = 0.10 if is_correction_year else 0.0
        
        for _ in range(TOTAL_STUDENTS_PER_YEAR):
            total_generated += 1
            student_id = f"S{str(year)[-2:]}_{total_generated:05d}"
            branch = np.random.choice(BRANCHES)
            
            # --- Academic Profile (Correlated) ---
            class_10 = np.clip(np.random.normal(80, 8), 50, 100)
            # Class 12 is strongly correlated with Class 10 (± noise)
            class_12 = np.clip(class_10 * 0.88 + np.random.normal(0, 5), 50, 100)
            # CGPA is correlated with Class 12 (± noise)
            cgpa_base = (class_12 / 10.0) + np.random.normal(0, 0.6)
            cgpa = np.clip(cgpa_base, 4.0, 10.0)
            
            # Active backlogs: higher probability for low CGPA
            if cgpa < 6.0:
                active_backlog = 1 if np.random.rand() < 0.35 else 0
            elif cgpa < 7.0:
                active_backlog = 1 if np.random.rand() < 0.12 else 0
            else:
                active_backlog = 1 if np.random.rand() < 0.02 else 0
                
            # --- Profile Extras (Correlated) ---
            # Internships: Poisson mean scaled by CGPA. Reduced during COVID.
            internship_mean = max(0.2, (cgpa - 4.5) * 0.38) * (1.0 - covid_internship_drop)
            internships = int(np.clip(np.random.poisson(internship_mean), 0, 5))
            
            # Research papers: High CGPA students are much more likely
            if cgpa >= 8.5:
                research_papers = int(np.clip(np.random.poisson(0.55), 0, 4))
            elif cgpa >= 7.5:
                research_papers = int(np.clip(np.random.poisson(0.12), 0, 2))
            else:
                research_papers = 0
                
            # Project Domains and Skills (Aligned by branch)
            if branch in ['CSE', 'IT']:
                domains = BRANCH_DOMAINS['CSE_IT']
            elif branch in ['ECE', 'EE']:
                domains = BRANCH_DOMAINS['ECE_EE']
            elif branch in ['ME', 'CE']:
                domains = BRANCH_DOMAINS['ME_CE']
            else: # BT
                domains = BRANCH_DOMAINS['BT']
                
            domain = np.random.choice(domains)
            
            # Choose 2 to 5 skills from branch skill pool
            branch_skills_pool = BRANCH_SKILLS[branch]
            skills_count = np.random.randint(2, 6)
            skills = ", ".join(np.random.choice(branch_skills_pool, size=skills_count, replace=False))
            
            # --- Target Intended Outcome (Behavioral Noise) ---
            # Preliminary probability weights for what the student wants to do
            # High CGPA + research papers -> higher chance of Higher Studies
            prob_higher = 0.05
            if cgpa > 8.5:
                prob_higher += 0.15
            if research_papers > 0:
                prob_higher += 0.20
            prob_higher = min(prob_higher, 0.50)
            
            # Entrepreneurship: 2% constant noise
            prob_entrepreneurship = 0.02
            
            # Placement intentions
            prob_placement = 1.0 - prob_higher - prob_entrepreneurship
            
            intended_path = np.random.choice(
                ['placement', 'higher_studies', 'entrepreneurship'], 
                p=[prob_placement, prob_higher, prob_entrepreneurship]
            )
            
            # --- Funnel Stage Variables (Strict Logical Consistency) ---
            eligible = 0
            registered = 0
            shortlisted = 0
            appeared = 0
            cleared = 0
            interviewed = 0
            offer_received = 0
            offer_accepted = 0
            joined_company = 0
            
            # Stage 1: Eligibility (affected heavily by active backlogs and CGPA)
            eligibility_chance = 0.98
            if active_backlog == 1:
                eligibility_chance = 0.20
            elif cgpa < 6.0:
                eligibility_chance = 0.40
            
            if np.random.rand() < eligibility_chance:
                eligible = 1
                
            # Stage 2: Registration (1 only if eligible = 1)
            if eligible == 1:
                # If they want higher studies/entrepreneurship, they rarely register. Else, they almost always do.
                if intended_path == 'higher_studies':
                    reg_chance = 0.15
                elif intended_path == 'entrepreneurship':
                    reg_chance = 0.05
                else:
                    reg_chance = 0.99
                
                if np.random.rand() < reg_chance:
                    registered = 1
                    
            # Stage 3: Shortlisting (1 only if registered = 1)
            if registered == 1:
                # Shortlisting probability depends on CGPA and internships
                # Backlogs hurt even if eligible
                shortlist_chance = 0.98
                if internships == 0:
                    shortlist_chance += 0.01
                elif internships in [1, 2]:
                    shortlist_chance += 0.02
                else: # 3+
                    shortlist_chance += 0.02
                    
                if cgpa >= 8.5:
                    shortlist_chance += 0.01
                elif cgpa < 6.5:
                    shortlist_chance -= 0.05
                    
                if active_backlog == 1:
                    shortlist_chance -= 0.10
                    
                shortlist_chance = np.clip(shortlist_chance, 0.60, 0.99)
                
                # COVID effect (less severe)
                if is_covid_year:
                    shortlist_chance *= 0.97
                    
                if np.random.rand() < shortlist_chance:
                    shortlisted = 1
                    
            # Stage 4: Appeared (1 only if shortlisted = 1)
            if shortlisted == 1:
                # Minor dropout (some skip test or got another offer off-campus)
                if np.random.rand() < 0.99:
                    appeared = 1
                    
            # Stage 5: Cleared Test/Rounds (1 only if appeared = 1)
            if appeared == 1:
                # Technical ability proxy = CGPA
                clear_chance = 0.98
                if cgpa >= 8.5:
                    clear_chance = 0.99
                elif cgpa >= 7.5:
                    clear_chance = 0.98
                elif cgpa < 6.5:
                    clear_chance = 0.85
                    
                if np.random.rand() < clear_chance:
                    cleared = 1
                    
            # Stage 6: Interviewed (1 only if cleared = 1)
            if cleared == 1:
                # 98% of cleared students proceed to interviews
                if np.random.rand() < 0.99:
                    interviewed = 1
                    
            # Stage 7: Offer Received (1 only if interviewed = 1)
            if interviewed == 1:
                # Offer chance (COVID and market dropouts apply)
                offer_chance = 0.97
                if cgpa >= 8.5:
                    offer_chance += 0.02
                if internships >= 2:
                    offer_chance += 0.01
                
                offer_chance = np.clip(offer_chance, 0.80, 0.99)
                offer_chance *= (1.0 - covid_hiring_drop * 0.1)
                offer_chance *= (1.0 - correction_drop * 0.1)
                
                if np.random.rand() < offer_chance:
                    offer_received = 1
                    
            # Stage 8: Offer Accepted (1 only if offer_received = 1)
            if offer_received == 1:
                # If they intended placement, they accept with 95% probability.
                # If they intended higher studies/entrepreneurship, they reject it (accept probability = 10%).
                if intended_path == 'placement':
                    accept_chance = 0.96
                else:
                    accept_chance = 0.08
                    
                if np.random.rand() < accept_chance:
                    offer_accepted = 1
                    
            # Stage 9: Joined Company (1 only if offer_accepted = 1)
            if offer_accepted == 1:
                # Offer accepted != always joined (reneges, better external offers, etc.)
                if np.random.rand() < 0.93:
                    joined_company = 1
                    
            # --- Placement Outcome ---
            outcome = 'Unplaced'
            placement_status = 'unplaced'
            company_name = ''
            company_type = ''
            company_tier = ''
            sector = ''
            package_lpa = 0.0
            
            # Map funnel actions back to final outcomes
            if offer_accepted == 1:
                outcome = 'Placed'
                placement_status = 'placed'
            elif intended_path == 'higher_studies':
                outcome = 'Higher Studies'
                placement_status = 'higher_studies'
            elif intended_path == 'entrepreneurship':
                outcome = 'Unplaced' # Maps to Unplaced in basic outcome for dashboard compatibility
                placement_status = 'entrepreneurship'
                
            # If they were eligible but unregistered, or registered but rejected, they can be Higher Studies/Entrepreneurship
            if outcome == 'Placed':
                # --- Match Recruiter and Package ---
                # Find eligible companies based on branch group and student profile
                # Filter companies by type preferences
                available_companies = list(COMPANIES.keys())
                
                # Weight company types based on Branch
                weights = []
                for c in available_companies:
                    ctype, ctier, csector = COMPANIES[c]
                    weight = 1.0
                    
                    # Branch matching core companies
                    if ctype == 'core':
                        if branch in ['ME', 'EE', 'CE']:
                            weight = 6.0
                        else:
                            weight = 0.05 # low chance for CS/IT/BT
                            
                    # Branch matching tech
                    if ctype == 'product':
                        if branch in ['CSE', 'IT']:
                            weight = 4.0
                        elif branch == 'ECE':
                            weight = 2.0
                        else:
                            weight = 0.1
                            
                    # CGPA checks for top tiers
                    if ctier == 'tier_1':
                        if cgpa >= 8.5:
                            weight *= 3.0
                        elif cgpa >= 7.5:
                            weight *= 0.5
                        else:
                            weight *= 0.0 # Tier 1 product/consulting doesn't hire below 7.5
                            
                    if ctier == 'tier_2':
                        if cgpa >= 7.0:
                            weight *= 1.5
                        else:
                            weight *= 0.1
                            
                    # COVID modifications
                    if is_covid_year:
                        if ctype == 'startup':
                            weight *= 0.5
                        elif ctype == 'product' and ctier == 'tier_1':
                            weight *= 0.7
                            
                    # Startup boom (2022, 2023)
                    if is_post_covid_boom and ctype == 'startup':
                        weight *= startup_boom_factor
                        
                    weights.append(weight)
                    
                # Normalize weights
                sum_w = sum(weights)
                if sum_w == 0:
                    weights = [1.0] * len(available_companies)
                    sum_w = len(available_companies)
                probs = [w / sum_w for w in weights]
                
                company_name = np.random.choice(available_companies, p=probs)
                company_type, company_tier, sector = COMPANIES[company_name]
                
                # Generate package
                package_lpa = generate_skewed_package(company_type, company_tier, inflation_factor, covid_hiring_drop)
                
            recruiter_visit_year = year if company_name else ""
            is_repeat = 1 if company_name and np.random.rand() < 0.65 else 0
            
            # Internship PPO conversion logic
            ppo_converted = 0
            if outcome == 'Placed' and internships > 0:
                # If CGPA is high and completed internships, 15% chance of PPO
                ppo_chance = 0.05 + internships * 0.08
                if cgpa >= 8.5:
                    ppo_chance += 0.10
                if np.random.rand() < ppo_chance:
                    ppo_converted = 1
                    
            records.append({
                # Core keys
                'student_id': student_id,
                'graduation_year': year,
                'branch': branch,
                'cgpa': round(cgpa, 2),
                'class_10_percent': round(class_10, 2),
                'class_12_percent': round(class_12, 2),
                'internships': internships,
                'research_papers': research_papers,
                'major_project_domain': domain,
                'skills': skills,
                'outcome': outcome,
                'company_name': company_name,
                'company_type': company_type,
                'sector': sector,
                'package_lpa': package_lpa,
                'active_backlogs': active_backlog,
                
                # User-requested 0/1 Funnel columns
                'eligible': eligible,
                'registered': registered,
                'shortlisted': shortlisted,
                'appeared': appeared,
                'cleared': cleared,
                'interviewed': interviewed,
                'offer_received': offer_received,
                'offer_accepted': offer_accepted,
                'joined_company': joined_company,
                
                # Duplicate columns for dashboard compatibility
                'eligible_for_placements': eligible,
                'registered_for_placements': registered,
                'appeared_for_test': appeared,
                'cleared_test': cleared,
                'internship_converted_to_ppo': ppo_converted,
                'is_repeat_recruiter': is_repeat,
                'recruiter_visit_year': recruiter_visit_year,
                
                # Additional Outcome schema
                'placement_status': placement_status,
                'company_tier': company_tier
            })
            
    df = pd.DataFrame(records)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    out_path = os.path.join('data', 'placement_data.csv')
    df.to_csv(out_path, index=False)
    
    print(f"Generated {len(df)} records.")
    print(f"Saved to {out_path}")
    print("\nSummary Statistics:")
    print(df['placement_status'].value_counts(normalize=True) * 100)
    print("\nPackage Stats (Placed):")
    placed_df = df[df['placement_status'] == 'placed']
    print(placed_df['package_lpa'].describe())
    
if __name__ == '__main__':
    generate_data()
