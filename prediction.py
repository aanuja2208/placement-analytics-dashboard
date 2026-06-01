import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle

class StudentOutcomePredictor:
    """Predict student outcomes using Logistic Regression"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.le_branch = LabelEncoder()
        self.le_domain = LabelEncoder()
        self.le_outcome = LabelEncoder()
        self.feature_names = None
        self.metrics = {}
    
    def prepare_data(self, df_students):
        """Prepare data for training"""
        df = df_students.copy()
        
        # Encode categorical variables
        df['branch_encoded'] = self.le_branch.fit_transform(df['branch'])
        df['domain_encoded'] = self.le_domain.fit_transform(df['major_project_domain'])
        
        # Select features
        features = ['cgpa', 'class_10_percent', 'class_12_percent', 
                   'internships_count', 'research_papers_count', 
                   'branch_encoded', 'domain_encoded']
        
        X = df[features]
        
        # Target: outcome (Placed, Higher Studies, Unplaced)
        y = df['outcome']
        y_encoded = self.le_outcome.fit_transform(y)
        
        self.feature_names = features
        
        return X, y_encoded, features
    
    def train(self, df_students):
        """Train the prediction model"""
        X, y, features = self.prepare_data(df_students)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = LogisticRegression(max_iter=1000, random_state=42, multi_class='multinomial')
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        
        self.metrics = {
            'accuracy': round(accuracy_score(y_test, y_pred), 3),
            'precision': round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 3),
            'recall': round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 3),
            'f1': round(f1_score(y_test, y_pred, average='weighted', zero_division=0), 3),
            'train_size': len(X_train),
            'test_size': len(X_test)
        }
        
        return self.metrics
    
    def predict_student(self, cgpa, class_10, class_12, internships, research_papers, 
                       branch, project_domain):
        """Predict outcome for a single student"""
        
        if self.model is None:
            return None
        
        # Encode inputs
        branch_enc = self.le_branch.transform([branch])[0]
        domain_enc = self.le_domain.transform([project_domain])[0]
        
        # Create feature vector
        features_array = np.array([[cgpa, class_10, class_12, internships, 
                                   research_papers, branch_enc, domain_enc]])
        
        # Scale
        features_scaled = self.scaler.transform(features_array)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Decode
        outcome = self.le_outcome.inverse_transform([prediction])[0]
        
        # Get probabilities for each class
        prob_dict = {
            'Placed': round(probabilities[self.le_outcome.transform(['Placed'])[0]] * 100, 1),
            'Higher Studies': round(probabilities[self.le_outcome.transform(['Higher Studies'])[0]] * 100, 1),
            'Unplaced': round(probabilities[self.le_outcome.transform(['Unplaced'])[0]] * 100, 1)
        }
        
        return {
            'predicted_outcome': outcome,
            'probabilities': prob_dict,
            'confidence': round(max(probabilities) * 100, 1)
        }
    
    def get_feature_importance(self):
        """Get feature importance from model coefficients"""
        if self.model is None:
            return None
        
        # For multinomial logistic regression, take mean absolute coefficients
        importance = np.abs(self.model.coef_).mean(axis=0)
        
        # Create dataframe
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        # Normalize to 0-100
        importance_df['importance'] = (importance_df['importance'] / importance_df['importance'].max() * 100).round(1)
        
        return importance_df
