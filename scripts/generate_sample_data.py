import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
years = range(2014, 2024)  # 10 years
branches = ['COE', 'EE', 'ECE', 'BT', 'ME']
domains = ['Software Systems', 'Core Engineering', 'Hardware & VLSI', 'Biotech Research', 
           'Data Science', 'IoT', 'Robotics', 'Web Development']
outcomes = ['Placed', 'Higher Studies', 'Unplaced']

# Generate 200 student records
students = []
student_counter = 1

for year in years:
    # ~20 students per year (10 years × 20 = 200)
    num_students = 20
    
    for i in range(num_students):
        # Generate realistic features
        cgpa = np.random.normal(7.5, 0.8)
        cgpa = np.clip(cgpa, 5.0, 10.0)
        
        class_10 = np.random.normal(82, 8)
        class_10 = np.clip(class_10, 60, 100)
        
        class_12 = np.random.normal(80, 8)
        class_12 = np.clip(class_12, 60, 100)
        
        internships = np.random.poisson(1)  # Most have 0-2 internships
        research_papers = max(0, np.random.poisson(0.3))
        
        # Outcome logic: higher CGPA → higher chance of placement
        rand = np.random.random()
        if cgpa > 8.5:
            outcome = 'Placed' if rand < 0.85 else ('Higher Studies' if rand < 0.95 else 'Unplaced')
        elif cgpa > 7.5:
            outcome = 'Placed' if rand < 0.70 else ('Higher Studies' if rand < 0.85 else 'Unplaced')
        elif cgpa > 7.0:
            outcome = 'Placed' if rand < 0.55 else ('Higher Studies' if rand < 0.75 else 'Unplaced')
        else:
            outcome = 'Placed' if rand < 0.35 else ('Higher Studies' if rand < 0.50 else 'Unplaced')
        
        branch = np.random.choice(branches)
        domain = np.random.choice(domains)
        
        students.append({
            'student_id': f'S{str(year)[-2:]}_{str(student_counter).zfill(2)}',
            'graduation_year': year,
            'branch': branch,
            'cgpa': round(cgpa, 2),
            'class_10_percent': round(class_10, 1),
            'class_12_percent': round(class_12, 1),
            'internships_count': int(internships),
            'major_project_domain': domain,
            'research_papers_count': int(research_papers),
            'outcome': outcome,
            'placed_flag': 1 if outcome == 'Placed' else 0,
            'higher_studies_flag': 1 if outcome == 'Higher Studies' else 0,
            'unplaced_flag': 1 if outcome == 'Unplaced' else 0
        })
        student_counter += 1

# Create DataFrame
df_students = pd.DataFrame(students)

# Save to CSV
df_students.to_csv('/home/claude/placement_project/data/students.csv', index=False)
print(f"✓ Generated {len(df_students)} student records")
print(df_students.head())

# Generate yearly aggregated data
yearly_data = []
for year in years:
    year_data = df_students[df_students['graduation_year'] == year]
    total = len(year_data)
    placed = year_data['placed_flag'].sum()
    higher_studies = year_data['higher_studies_flag'].sum()
    unplaced = year_data['unplaced_flag'].sum()
    
    # Simulated package data (realistic ranges)
    packages = np.random.normal(6.0, 1.5, max(1, int(placed)))
    packages = np.clip(packages, 3.5, 12.0)
    median_pkg = np.median(packages) if len(packages) > 0 else 0
    avg_pkg = np.mean(packages) if len(packages) > 0 else 0
    
    yearly_data.append({
        'graduation_year': year,
        'total_students': total,
        'placed_students': int(placed),
        'placement_rate_pct': round((placed / total * 100) if total > 0 else 0, 1),
        'higher_studies_students': int(higher_studies),
        'higher_studies_rate_pct': round((higher_studies / total * 100) if total > 0 else 0, 1),
        'unplaced_students': int(unplaced),
        'unplaced_rate_pct': round((unplaced / total * 100) if total > 0 else 0, 1),
        'median_package_lpa': round(median_pkg, 2),
        'average_package_lpa': round(avg_pkg, 2),
        'average_cgpa': round(year_data['cgpa'].mean(), 2),
        'average_internships': round(year_data['internships_count'].mean(), 2)
    })

df_yearly = pd.DataFrame(yearly_data)
df_yearly.to_csv('/home/claude/placement_project/data/yearly_outcomes.csv', index=False)
print(f"\n✓ Generated yearly aggregated data (10 years)")
print(df_yearly.head())
