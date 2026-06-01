# 📊 Campus Placement Analytics & Forecasting Dashboard

A simple, practical machine learning and analytics system for analyzing student placement outcomes and forecasting future trends in an engineering university.

## 🎯 Project Overview

This project provides:
- **Time-series forecasting** of placement rates, package trends, and higher studies rates
- **Student-level analysis** of placement drivers (CGPA, internships, branch, etc.)
- **Interactive Streamlit dashboard** with 6 pages of insights and visualizations
- **Student outcome predictor** to estimate placement probability based on student profile
- **100% self-contained** in a single Streamlit app

## 📁 Project Structure

```
placement_project/
├── data/
│   ├── students.csv              # 200 student records (one row per student)
│   └── yearly_outcomes.csv       # Aggregated yearly data (10 years)
├── scripts/
│   ├── generate_sample_data.py   # Generate synthetic dataset
│   ├── data_processing.py        # Data analysis utilities
│   ├── forecasting.py            # Time-series forecasting models
│   └── prediction.py             # Student outcome classifier
├── app.py                        # Main Streamlit application (all-in-one)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data (if not already present)

```bash
python scripts/generate_sample_data.py
```

This creates:
- `data/students.csv` - 200 sample student records (2014-2023)
- `data/yearly_outcomes.csv` - Aggregated yearly statistics

### 3. Run the Dashboard

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Dashboard Pages

### 1. 🏠 Executive Overview
- Key KPIs: Total students, placement rate, higher studies rate, unplaced rate
- Outcome distribution pie chart
- 10-year placement rate trend

### 2. 📈 Placement Trends
- Placement rate over time
- Higher studies rate trend
- Unplaced rate trend
- Median and average package trends
- Detailed yearly data table

### 3. 🎓 Branch Analysis
- Branch-wise placement rates
- Student distribution by branch
- Average CGPA and internships by branch
- Performance comparison across all branches

### 4. 📊 Student Profiles
- **CGPA Band Analysis**: Placement rate by CGPA ranges
- **Internship Analysis**: Impact of internship count on placement
- Outcome breakdown by profile metrics

### 5. 🔮 Forecasting
- Placement rate forecast (3 years ahead)
- Higher studies rate forecast
- Package trend forecast
- Historical vs. forecasted comparison charts

### 6. 🤖 Student Predictor
- Predict individual student outcome based on profile
- Model performance metrics (accuracy, precision, recall, F1)
- Feature importance visualization
- Probability breakdown for each outcome

## 🔧 Technical Components

### Data Processing (`scripts/data_processing.py`)
- Load and clean student and yearly data
- Aggregate student-level data into yearly summaries
- Generate branch-wise, CGPA-wise, and internship-wise analysis

### Forecasting (`scripts/forecasting.py`)
- **SimpleForecaster class** with two methods:
  - **Moving Average**: Uses last 3 data points to forecast
  - **Exponential Smoothing**: Weighted average with trend
- Forecasts: Placement rate, package, higher studies rate
- Supports multi-year forecasting

### Prediction Model (`scripts/prediction.py`)
- **Logistic Regression** classifier (multinomial)
- Features: CGPA, class marks, internships, research papers, branch, project domain
- Outputs: Predicted outcome + probability for each class
- Provides feature importance ranking

## 📈 Key Features

✅ **Simple but effective ML**
- No deep learning or complex algorithms
- Transparent, interpretable models
- Suitable for 10 years of data

✅ **Interactive visualizations**
- Plotly charts for rich interactivity
- Real-time filters and inputs
- Professional dashboard design

✅ **Comprehensive analysis**
- Student-level insights
- Time-series trends
- Profile-based breakdowns
- Forecasting capabilities

✅ **Single Streamlit app**
- All features in one place
- No frontend/backend separation
- Easy to deploy and share

## 📊 Data Schema

### students.csv
| Column | Type | Description |
|--------|------|-------------|
| student_id | str | Unique identifier |
| graduation_year | int | Year of graduation (2014-2023) |
| branch | str | Academic branch (COE, EE, ECE, BT, ME) |
| cgpa | float | Final CGPA (0-10) |
| class_10_percent | float | Class 10 score (0-100) |
| class_12_percent | float | Class 12 score (0-100) |
| internships_count | int | Number of internships (0-5) |
| major_project_domain | str | Project area |
| research_papers_count | int | Number of published papers |
| outcome | str | Placed / Higher Studies / Unplaced |
| placed_flag | int | 1 if placed, 0 otherwise |
| higher_studies_flag | int | 1 if pursuing higher studies, 0 otherwise |
| unplaced_flag | int | 1 if unplaced, 0 otherwise |

### yearly_outcomes.csv
| Column | Type | Description |
|--------|------|-------------|
| graduation_year | int | Year |
| total_students | int | Total graduating students |
| placed_students | int | Number placed |
| placement_rate_pct | float | Placement % |
| higher_studies_students | int | Students in higher studies |
| higher_studies_rate_pct | float | Higher studies % |
| unplaced_students | int | Unplaced students |
| unplaced_rate_pct | float | Unplaced % |
| median_package_lpa | float | Median salary package |
| average_package_lpa | float | Average salary package |
| average_cgpa | float | Batch avg CGPA |
| average_internships | float | Avg internships per student |

## 🎓 Machine Learning Models

### 1. Time-Series Forecasting
**Algorithm**: Moving Average + Trend Extrapolation

Why this approach?
- Only ~10 annual data points available
- Simple, interpretable, and suitable for this data size
- Captures trend without overfitting

**Forecasted Metrics**:
- Placement rate
- Package trends (median & average)
- Higher studies rate
- Unplaced rate

### 2. Student Outcome Classification
**Algorithm**: Logistic Regression (multinomial)

Why this approach?
- Fast, interpretable, and reliable
- Works well with mixed feature types
- Provides probability estimates
- Feature importance is clear

**Input Features**:
- CGPA
- Class 10 & 12 marks
- Internship count
- Research papers
- Branch (encoded)
- Project domain (encoded)

**Target Classes**:
- Placed
- Higher Studies
- Unplaced

## 📈 Evaluation Metrics

### Forecasting
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)

### Classification
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-Score (weighted)

## 🔄 Workflow

1. **Data Generation** → Generate synthetic 200-student dataset
2. **Exploratory Analysis** → Dashboard Pages 2, 3, 4
3. **Trend Analysis** → Dashboard Page 2
4. **Forecasting** → Dashboard Page 5
5. **Individual Prediction** → Dashboard Page 6

## 🛠️ Customization

### Using Your Own Data

Replace `data/students.csv` with your actual dataset. Ensure it has the same columns.

Then run:
```bash
streamlit run app.py
```

The app will automatically:
1. Load your data
2. Aggregate into yearly summaries
3. Train the ML models
4. Generate all visualizations

### Modifying Forecast Period

In `app.py`, change the `years_ahead` parameter:
```python
forecasts = forecast_all_metrics(df_yearly, years_ahead=5)  # Forecast 5 years instead of 3
```

### Adjusting Model Parameters

**Forecasting** (`scripts/forecasting.py`):
- Modify `window` parameter in `moving_average()` for different smoothing
- Adjust `alpha` in `exponential_smoothing()` for faster/slower decay

**Prediction** (`scripts/prediction.py`):
- Adjust `test_size` in `train_test_split()` (default: 0.2)
- Change `max_iter` in LogisticRegression if model doesn't converge

## ⚠️ Limitations

- Only 10 annual observations limit forecasting sophistication
- Synthetic data for demonstration (replace with real university data)
- Student profiles simplified to key metrics
- Startup outcomes not separately tracked
- Model for analytical insights, not official decisions

## 🎯 Expected Performance

With sample data:
- **Forecasting Accuracy**: ±5-10% MAPE on trends
- **Classification Accuracy**: 70-80% overall
- **Dashboard Load Time**: <2 seconds

## 📝 Sample Output

```
Executive Summary:
- Total Students: 200
- Placement Rate: 72.5%
- Higher Studies Rate: 15.0%
- Unplaced Rate: 12.5%
- Average Package: 6.2 LPA

Top Branch (Placement):
- COE: 78% placement rate
- EE: 71% placement rate
- ECE: 68% placement rate
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Deploy from GitHub repo

### Docker
```bash
docker run -p 8501:8501 -v $(pwd):/app streamlit/streamlit-app
```

## 📚 Dependencies

- **streamlit**: Web framework
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **scikit-learn**: ML models & metrics
- **plotly**: Interactive visualizations

## 📄 License

Free to use for educational purposes.

## 🤝 Contributing

Suggest improvements via:
1. Data quality enhancements
2. Additional visualizations
3. More sophisticated forecasting
4. Better feature engineering

## ❓ Troubleshooting

**Q: "Data files not found" error**
A: Run `python scripts/generate_sample_data.py` to create sample data

**Q: Streamlit doesn't load**
A: Ensure all requirements are installed: `pip install -r requirements.txt`

**Q: Prediction model accuracy is low**
A: This is expected with synthetic data. Use real institutional data for better results.

## 📞 Support

For issues or questions, check:
- Streamlit docs: https://docs.streamlit.io
- Scikit-learn docs: https://scikit-learn.org
- Plotly docs: https://plotly.com/python

---

**Built for**: Simple, practical campus placement analytics
**Complexity Level**: Beginner-friendly
**Time to Run**: ~2 minutes (data generation) + 30 seconds (dashboard)
