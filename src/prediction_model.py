"""
Student Outcome Prediction Model using Random Forest Classifier.
Handles training, prediction, feature importance, and probability estimation.
Designed to scale efficiently with large datasets (10,000+ records).
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import os

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')


class StudentOutcomePredictor:
    """Predict student placement outcomes using Random Forest."""

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.encoders = {}
        self.feature_names = []
        self.metrics = {}
        self.outcome_classes = ['Higher Studies', 'Placed', 'Unplaced']

    # ----- data preparation -----
    def _encode_column(self, series, col_name, fit=True):
        """Encode a categorical column. Creates encoder if fitting."""
        if fit:
            le = LabelEncoder()
            encoded = le.fit_transform(series.astype(str))
            self.encoders[col_name] = le
        else:
            le = self.encoders.get(col_name)
            if le is None:
                return np.zeros(len(series), dtype=int)
            # handle unseen labels gracefully
            mapping = {label: idx for idx, label in enumerate(le.classes_)}
            encoded = series.astype(str).map(mapping).fillna(0).astype(int)
        return encoded

    def _prepare_features(self, df, fit=True):
        """Extract and encode feature matrix from dataframe."""
        data = df.copy()

        # Numeric features
        numeric_cols = ['cgpa', 'class_10_percent', 'class_12_percent',
                        'internships', 'research_papers']
        for col in numeric_cols:
            if col not in data.columns:
                data[col] = 0

        # Categorical features
        cat_cols = ['branch', 'major_project_domain']
        for col in cat_cols:
            enc_col = f'{col}_encoded'
            if col in data.columns:
                data[enc_col] = self._encode_column(data[col], col, fit=fit)
            else:
                data[enc_col] = 0

        feature_cols = numeric_cols + [f'{c}_encoded' for c in cat_cols]
        self.feature_names = feature_cols
        return data[feature_cols].values

    # ----- training -----
    def train(self, df):
        """Train the model on the full dataset. Returns metrics dict."""
        if df.empty or 'outcome' not in df.columns:
            return {'accuracy': 0, 'note': 'No data provided'}

        X = self._prepare_features(df, fit=True)
        y = self._encode_column(df['outcome'], 'outcome', fit=True)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model = RandomForestClassifier(
            n_estimators=150, max_depth=12, min_samples_split=5,
            min_samples_leaf=3, random_state=42, n_jobs=-1,
        )
        self.model.fit(X_train_scaled, y_train)

        y_pred = self.model.predict(X_test_scaled)
        self.outcome_classes = list(self.encoders['outcome'].classes_)

        self.metrics = {
            'accuracy': round(accuracy_score(y_test, y_pred), 3),
            'precision': round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 3),
            'recall': round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 3),
            'f1': round(f1_score(y_test, y_pred, average='weighted', zero_division=0), 3),
            'train_size': len(X_train),
            'test_size': len(X_test),
        }
        return self.metrics

    # ----- prediction -----
    def predict(self, cgpa, class_10, class_12, internships, research_papers,
                branch, project_domain):
        """Predict outcome for a single student. Returns dict with outcome and probabilities."""
        if self.model is None:
            return None

        row = pd.DataFrame([{
            'cgpa': cgpa,
            'class_10_percent': class_10,
            'class_12_percent': class_12,
            'internships': internships,
            'research_papers': research_papers,
            'branch': branch,
            'major_project_domain': project_domain,
        }])

        X = self._prepare_features(row, fit=False)
        X_scaled = self.scaler.transform(X)

        prediction_idx = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]

        outcome = self.encoders['outcome'].inverse_transform([prediction_idx])[0]

        prob_dict = {}
        for i, cls in enumerate(self.outcome_classes):
            prob_dict[cls] = round(float(probabilities[i]) * 100, 1)

        return {
            'predicted_outcome': outcome,
            'probabilities': prob_dict,
            'confidence': round(float(max(probabilities)) * 100, 1),
        }

    # ----- feature importance -----
    def get_feature_importance(self):
        """Return feature importance as a sorted DataFrame (0-100 scale)."""
        if self.model is None:
            return pd.DataFrame(columns=['feature', 'importance'])

        importance = self.model.feature_importances_
        df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance,
        }).sort_values('importance', ascending=False)

        max_val = df['importance'].max()
        if max_val > 0:
            df['importance'] = (df['importance'] / max_val * 100).round(1)

        # Clean up feature names for display
        df['feature_display'] = df['feature'].str.replace('_encoded', '').str.replace('_', ' ').str.title()
        return df.reset_index(drop=True)

    # ----- persistence -----
    def save(self, path=None):
        """Save model to disk."""
        os.makedirs(MODEL_DIR, exist_ok=True)
        path = path or os.path.join(MODEL_DIR, 'outcome_predictor.pkl')
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'encoders': self.encoders,
                'feature_names': self.feature_names,
                'metrics': self.metrics,
                'outcome_classes': self.outcome_classes,
            }, f)

    def load(self, path=None):
        """Load model from disk. Returns True if successful."""
        path = path or os.path.join(MODEL_DIR, 'outcome_predictor.pkl')
        if not os.path.exists(path):
            return False
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.model = data['model']
        self.scaler = data['scaler']
        self.encoders = data['encoders']
        self.feature_names = data['feature_names']
        self.metrics = data.get('metrics', {})
        self.outcome_classes = data.get('outcome_classes', ['Higher Studies', 'Placed', 'Unplaced'])
        return True
