"""
Student Recommendation Engine.
Provides actionable improvement suggestions based on a student's profile
compared to aggregate placement data.
"""

import pandas as pd
import numpy as np


class RecommendationEngine:
    """Generate data-driven recommendations for individual students."""

    def __init__(self, df):
        """Initialize with the full placement dataset for benchmarking."""
        self.full_df = df.copy()
        placed = df[df['outcome'] == 'Placed']
        self.placed_df = placed.copy()
        self.benchmarks = {
            'cgpa_median': placed['cgpa'].median() if not placed.empty else 7.5,
            'cgpa_75': placed['cgpa'].quantile(0.75) if not placed.empty else 8.0,
            'internship_median': placed['internships'].median() if not placed.empty else 1,
            'research_median': placed['research_papers'].median() if not placed.empty else 0,
            'class_10_median': placed['class_10_percent'].median() if not placed.empty else 80,
            'class_12_median': placed['class_12_percent'].median() if not placed.empty else 78,
        }
        # Branch-company affinity
        self._build_branch_affinity(df)
        # Sector package stats
        self._build_sector_stats(placed)

    def _build_branch_affinity(self, df):
        """Compute which company types hire most from each branch."""
        if 'company_type' not in df.columns or df.empty:
            self.branch_affinity = {}
            return
        placed = df[df['outcome'] == 'Placed']
        if placed.empty:
            self.branch_affinity = {}
            return
        ct = pd.crosstab(placed['branch'], placed['company_type'], normalize='index')
        self.branch_affinity = ct.to_dict(orient='index')

    def _build_sector_stats(self, placed):
        """Average package by sector for targeting suggestions."""
        if placed.empty or 'sector' not in placed.columns:
            self.sector_stats = pd.DataFrame()
            return
        self.sector_stats = (
            placed.groupby('sector')['package_lpa']
            .agg(['mean', 'median', 'count'])
            .sort_values('median', ascending=False)
            .reset_index()
        )

    # ----- public API -----
    def get_readiness(self, cgpa, internships, research_papers, class_10, class_12):
        """Return readiness category and score (0-100)."""
        score = 0.0
        # CGPA contribution (40%)
        cgpa_score = min((cgpa / self.benchmarks['cgpa_75']) * 100, 100)
        score += cgpa_score * 0.40

        # Internship contribution (25%)
        int_target = max(self.benchmarks['internship_median'], 1)
        int_score = min((internships / int_target) * 100, 100)
        score += int_score * 0.25

        # Academic background (20%)
        acad = (class_10 + class_12) / 2
        acad_target = (self.benchmarks['class_10_median'] + self.benchmarks['class_12_median']) / 2
        acad_score = min((acad / acad_target) * 100, 100) if acad_target > 0 else 50
        score += acad_score * 0.20

        # Research (15%)
        res_target = max(self.benchmarks['research_median'], 1)
        res_score = min((research_papers / res_target) * 100, 100)
        score += res_score * 0.15

        score = round(min(score, 100), 1)

        if score >= 80:
            category = 'HIGHLY READY'
        elif score >= 60:
            category = 'MODERATELY READY'
        elif score >= 40:
            category = 'NEEDS IMPROVEMENT'
        else:
            category = 'AT RISK'

        return category, score

    def get_strengths(self, cgpa, internships, research_papers, class_10, class_12):
        """List student strengths based on benchmarks."""
        strengths = []
        if cgpa >= self.benchmarks['cgpa_75']:
            strengths.append('Strong CGPA (above 75th percentile of placed students)')
        elif cgpa >= self.benchmarks['cgpa_median']:
            strengths.append('Above-average CGPA compared to placed students')
        if internships >= 2:
            strengths.append(f'Good internship experience ({internships} internships)')
        elif internships >= 1:
            strengths.append('Has internship experience')
        if research_papers >= 1:
            strengths.append(f'Research publications ({research_papers} papers)')
        if class_10 >= 85:
            strengths.append('Strong Class 10 academic record')
        if class_12 >= 85:
            strengths.append('Strong Class 12 academic record')
        return strengths

    def get_weaknesses(self, cgpa, internships, research_papers, class_10, class_12):
        """List areas needing improvement."""
        weaknesses = []
        if cgpa < self.benchmarks['cgpa_median']:
            weaknesses.append(
                f'CGPA ({cgpa:.1f}) below placed-student median ({self.benchmarks["cgpa_median"]:.1f})'
            )
        if internships == 0:
            weaknesses.append('No internship experience')
        if research_papers == 0 and self.benchmarks['research_median'] > 0:
            weaknesses.append('No research papers')
        if class_10 < 70:
            weaknesses.append('Below-average Class 10 performance')
        if class_12 < 70:
            weaknesses.append('Below-average Class 12 performance')
        return weaknesses

    def get_actions(self, cgpa, internships, research_papers, branch, class_10, class_12):
        """Generate actionable recommendations."""
        actions = []
        priority = 1

        if cgpa < 7.0:
            actions.append({
                'priority': priority,
                'area': 'CGPA',
                'action': f'Focus on improving CGPA from {cgpa:.1f} to at least 7.5. '
                          f'Target courses where improvement is feasible.',
            })
            priority += 1
        elif cgpa < 7.5:
            actions.append({
                'priority': priority,
                'area': 'CGPA',
                'action': f'Push CGPA from {cgpa:.1f} toward 8.0 for access to top recruiters.',
            })
            priority += 1

        if internships == 0:
            actions.append({
                'priority': priority,
                'area': 'Internship',
                'action': 'Complete at least one industry internship before placement season. '
                          'Target companies aligned with your branch.',
            })
            priority += 1
        elif internships == 1:
            actions.append({
                'priority': priority,
                'area': 'Internship',
                'action': 'Consider a second internship or a PPO-track position to strengthen your profile.',
            })
            priority += 1

        if research_papers == 0:
            actions.append({
                'priority': priority,
                'area': 'Projects',
                'action': 'Work on a capstone or domain-specific project that demonstrates applied skills. '
                          'Consider publishing a conference paper.',
            })
            priority += 1

        # Skill suggestions based on branch
        skill_map = {
            'CSE': 'Python, Data Structures, System Design, Cloud platforms',
            'IT': 'Full-stack development, DevOps, Cloud computing',
            'ECE': 'Embedded Systems, VLSI, Signal Processing, Python',
            'EE': 'Power Systems, Control Systems, MATLAB, IoT',
            'ME': 'CAD/CAM, Finite Element Analysis, AutoCAD, Solidworks',
            'CE': 'Structural Analysis, AutoCAD, Project Management',
            'BT': 'Bioinformatics, Data Analysis, R, Lab techniques',
        }
        suggested = skill_map.get(branch, 'Technical skills relevant to your field')
        actions.append({
            'priority': priority,
            'area': 'Skills',
            'action': f'Strengthen key skills: {suggested}',
        })

        return actions

    def get_suggested_sectors(self, branch, cgpa):
        """Suggest company categories based on branch affinity and CGPA."""
        suggestions = []

        if branch in self.branch_affinity:
            affinity = self.branch_affinity[branch]
            sorted_types = sorted(affinity.items(), key=lambda x: x[1], reverse=True)
            for ctype, pct in sorted_types[:3]:
                if pct > 0.05:
                    suggestions.append({
                        'type': ctype,
                        'match': f'{pct * 100:.0f}% of placed {branch} students',
                    })

        if cgpa >= 8.0:
            suggestions.append({'type': 'Product-based / High-tier', 'match': 'CGPA qualifies'})
        elif cgpa >= 7.0:
            suggestions.append({'type': 'Service / Mid-tier', 'match': 'CGPA competitive'})

        return suggestions

    def get_target_companies(self, branch, cgpa, internships=0, top_n=10):
        """Suggest specific companies to target based on student profile.

        Filters placed students by branch and CGPA proximity, then ranks
        companies by historical hiring volume and package. Returns a list
        of dicts with company details including sector.
        """
        if self.placed_df.empty:
            return []

        placed = self.placed_df.copy()

        # Filter to companies that have hired from this branch
        branch_placed = placed[placed['branch'] == branch]
        if branch_placed.empty:
            branch_placed = placed  # Fallback: use all data

        # CGPA-tier matching: find companies that hire students with similar CGPAs
        # Allow a band of +/- 1.0 around the student's CGPA
        cgpa_low = max(cgpa - 1.0, 0)
        cgpa_high = min(cgpa + 1.5, 10.0)
        tier_placed = branch_placed[
            (branch_placed['cgpa'] >= cgpa_low) & (branch_placed['cgpa'] <= cgpa_high)
        ]
        if len(tier_placed) < 5:
            tier_placed = branch_placed  # Fallback if too few matches

        # Filter out rows with no company name
        tier_placed = tier_placed[tier_placed['company_name'].str.strip() != '']

        if tier_placed.empty:
            return []

        # Aggregate by company
        required_cols = ['company_name']
        agg_dict = {'package_lpa': 'mean', 'student_id': 'count'}

        # Build company summary
        company_summary = tier_placed.groupby('company_name').agg(
            avg_package=('package_lpa', 'mean'),
            hires=('student_id', 'count'),
            sector=('sector', lambda s: s.mode().iloc[0] if not s.mode().empty else 'N/A'),
            company_type=('company_type', lambda s: s.mode().iloc[0] if not s.mode().empty else 'N/A'),
        ).reset_index()

        # Add tier info if available
        if 'company_tier' in tier_placed.columns:
            tier_info = tier_placed.groupby('company_name')['company_tier'].agg(
                lambda s: s.mode().iloc[0] if not s.mode().empty else 'N/A'
            ).reset_index()
            tier_info.columns = ['company_name', 'tier']
            company_summary = company_summary.merge(tier_info, on='company_name', how='left')
        else:
            company_summary['tier'] = 'N/A'

        # Score companies: weighted by hires (reliability) and package (value)
        if company_summary['avg_package'].max() > 0:
            company_summary['pkg_score'] = company_summary['avg_package'] / company_summary['avg_package'].max()
        else:
            company_summary['pkg_score'] = 0
        if company_summary['hires'].max() > 0:
            company_summary['hire_score'] = company_summary['hires'] / company_summary['hires'].max()
        else:
            company_summary['hire_score'] = 0

        company_summary['score'] = company_summary['pkg_score'] * 0.4 + company_summary['hire_score'] * 0.6
        company_summary = company_summary.sort_values('score', ascending=False).head(top_n)

        results = []
        for _, row in company_summary.iterrows():
            results.append({
                'company': row['company_name'],
                'sector': row['sector'] if row['sector'] else 'N/A',
                'type': row['company_type'] if row['company_type'] else 'N/A',
                'tier': row.get('tier', 'N/A') if row.get('tier', '') else 'N/A',
                'avg_package': round(row['avg_package'], 2),
                'hires': int(row['hires']),
            })

        return results

