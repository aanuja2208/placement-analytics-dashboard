import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.prediction_model import StudentOutcomePredictor
from src.recommendation_engine import RecommendationEngine
import src.visualizations as vis
from src.utils import get_kpi_card_html

st.set_page_config(page_title="Student Predictor & Recommendations", layout="wide")

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

st.title("Student Predictor & Recommendation Engine")
st.markdown("Predict individual student outcomes and generate personalized improvement plans.")

# Initialize and train model if not already done
@st.cache_resource
def get_trained_predictor(data):
    predictor = StudentOutcomePredictor()
    predictor.train(data)
    return predictor

@st.cache_resource
def get_recommender(data):
    return RecommendationEngine(data)

predictor = get_trained_predictor(df)
recommender = get_recommender(df)

with st.sidebar:
    st.header("Student Profile Input")
    cgpa = st.slider("CGPA", 4.0, 10.0, 7.5, 0.1)
    class_10 = st.slider("Class 10 (%)", 45.0, 100.0, 80.0, 1.0)
    class_12 = st.slider("Class 12 (%)", 45.0, 100.0, 75.0, 1.0)
    internships = st.number_input("Internships", 0, 5, 1)
    research_papers = st.number_input("Research Papers", 0, 5, 0)
    branch = st.selectbox("Branch", sorted(df['branch'].unique()))
    domain = st.selectbox("Major Project Domain", sorted(df['major_project_domain'].unique()))
    
    predict_btn = st.button("Generate Prediction & Plan", type="primary", use_container_width=True)

if predict_btn:
    st.markdown("---")
    
    # Get Predictions
    pred = predictor.predict(cgpa, class_10, class_12, internships, research_papers, branch, domain)
    
    # Get Recommendations
    category, readiness_score = recommender.get_readiness(cgpa, internships, research_papers, class_10, class_12)
    strengths = recommender.get_strengths(cgpa, internships, research_papers, class_10, class_12)
    weaknesses = recommender.get_weaknesses(cgpa, internships, research_papers, class_10, class_12)
    actions = recommender.get_actions(cgpa, internships, research_papers, branch, class_10, class_12)
    suggested_sectors = recommender.get_suggested_sectors(branch, cgpa)
    target_companies = recommender.get_target_companies(branch, cgpa, internships)
    
    # Display Top Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        color = '#22A06B' if pred['predicted_outcome'] == 'Placed' else ('#2E86AB' if pred['predicted_outcome'] == 'Higher Studies' else '#BF2600')
        html = f"""<div style="background:#FFFFFF;border:1px solid #D1D5DB;border-radius:10px;padding:18px 20px;text-align:center;box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <div style="font-size:16px;color:#4B5563;text-transform:uppercase;font-weight:600;">Predicted Outcome</div>
        <div style="font-size:36px;font-weight:700;color:{color};margin-top:5px;">{pred['predicted_outcome']}</div>
        <div style="font-size:16px;color:{color};margin-top:5px;font-weight:600;">↑ Confidence: {pred['confidence']:.1f}%</div>
        </div>"""
        st.markdown(html, unsafe_allow_html=True)
        
    with c2: st.markdown(get_kpi_card_html("Placement Prob.", f"{pred['probabilities'].get('Placed', 0)}%"), unsafe_allow_html=True)
    with c3: st.markdown(get_kpi_card_html("Readiness Score", f"{readiness_score}/100"), unsafe_allow_html=True)
    
    with c4:
        cat_color = '#22A06B' if 'HIGHLY' in category else ('#F18F01' if 'MODERATE' in category else '#BF2600')
        html = f"""<div style="background:#FFFFFF;border:1px solid #D1D5DB;border-radius:10px;padding:18px 20px;text-align:center;box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <div style="font-size:16px;color:#4B5563;text-transform:uppercase;font-weight:600;">Readiness Category</div>
        <div style="font-size:36px;font-weight:700;color:{cat_color};margin-top:5px;">{category}</div>
        <div style="font-size:16px;color:{cat_color};margin-top:5px;font-weight:600;">Score: {readiness_score}/100</div>
        </div>"""
        st.markdown(html, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Profile Analysis")
        st.markdown("**Strengths:**")
        if strengths:
            for s in strengths: st.markdown(f"- {s}")
        else:
            st.markdown("- None identified based on benchmarks.")
            
        st.markdown("**Areas for Improvement:**")
        if weaknesses:
            for w in weaknesses: st.markdown(f"- {w}")
        else:
            st.markdown("- Profile looks solid across all benchmark areas.")
            
        st.markdown("### Suggested Target Sectors")
        if suggested_sectors:
            for s in suggested_sectors:
                st.markdown(f"- **{s['type']}** ({s['match']})")
                
    with col2:
        st.markdown("### Recommended Action Plan")
        for a in actions:
            st.info(f"**Priority {a['priority']} - {a['area']}:** {a['action']}")
    
    # --- Companies to Target Section ---
    st.markdown("---")
    st.markdown("### 🏢 Companies to Target")
    st.markdown("Based on your branch, CGPA, and historical placement patterns, these companies are the best fit for your profile.")
    
    if target_companies:
        # Build a styled table
        company_data = []
        for i, comp in enumerate(target_companies, 1):
            tier_label = comp['tier'].replace('_', ' ').title() if comp['tier'] != 'N/A' else '—'
            company_data.append({
                'Rank': i,
                'Company': comp['company'],
                'Sector': comp['sector'],
                'Type': comp['type'].title(),
                'Tier': tier_label,
                'Avg Package (LPA)': comp['avg_package'],
                'Historical Hires': comp['hires'],
            })
        
        company_table_df = pd.DataFrame(company_data)
        
        # Display with styled formatting
        st.dataframe(
            company_table_df.style.format({
                'Avg Package (LPA)': '{:.2f}',
            }).background_gradient(
                subset=['Avg Package (LPA)'], cmap='Greens'
            ).background_gradient(
                subset=['Historical Hires'], cmap='Blues'
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Companies to Target: Ranked using a composite score that weights historical hiring volume (60%) "
            "and average package offered (40%). Filtered to companies that have previously hired from your branch "
            "and students with a similar CGPA range (±1.0). 'Historical Hires' shows how many students with a "
            "similar profile were placed at that company."
        )
    else:
        st.info("No specific company recommendations available for the selected profile. Try adjusting your branch or CGPA.")

    st.markdown("---")
    st.markdown("### Machine Learning Insights")
    c3, c4 = st.columns(2)
    with c3:
        prob_df = pd.DataFrame(list(pred['probabilities'].items()), columns=['Outcome', 'Probability'])
        fig_prob = vis.bar_chart(prob_df, x='Outcome', y='Probability', title="Outcome Probabilities", text_auto=True)
        st.plotly_chart(fig_prob, use_container_width=True)
        st.caption("Outcome Probabilities: The Random Forest classifier outputs probability estimates for each outcome class based on the student's profile features. Higher bars indicate the model's confidence in that outcome. These probabilities are calibrated from 5,000 historical student records.")
        
    with c4:
        feat_imp = predictor.get_feature_importance().head(5)
        fig_feat = vis.bar_chart(feat_imp, x='importance', y='feature_display', horizontal=True, title="Key Factors (Feature Importance)")
        st.plotly_chart(fig_feat, use_container_width=True)
        st.caption("Key Factors (Feature Importance): Extracted from the trained Random Forest model, showing which input features contribute most to the prediction. Higher importance means the feature had greater impact on the decision trees' splits. CGPA typically dominates, followed by internship count.")
else:
    st.info("Fill the student profile on the sidebar and click **Generate Prediction**.")

