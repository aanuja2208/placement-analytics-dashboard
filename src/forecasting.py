"""
Forecasting module using Moving Average and Exponential Smoothing.
Provides multi-year forecasts for key placement metrics.
"""

import pandas as pd
import numpy as np


class PlacementForecaster:
    """Forecast placement metrics using simple time-series methods."""

    def __init__(self, years, values, metric_name='Metric'):
        self.years = np.array(years, dtype=int)
        self.values = np.array(values, dtype=float)
        self.metric_name = metric_name
        self.last_year = int(self.years[-1]) if len(self.years) > 0 else 2023

    def moving_average(self, window=3):
        """Simple Moving Average of last `window` observations."""
        if len(self.values) == 0:
            return 0.0
        w = min(window, len(self.values))
        return float(np.mean(self.values[-w:]))

    def exponential_smoothing(self, alpha=0.3):
        """Single Exponential Smoothing."""
        if len(self.values) == 0:
            return 0.0
        forecast = float(self.values[0])
        for v in self.values[1:]:
            forecast = alpha * float(v) + (1 - alpha) * forecast
        return forecast

    def linear_trend(self):
        """Compute slope from linear regression on the series."""
        if len(self.values) < 2:
            return 0.0
        x = np.arange(len(self.values), dtype=float)
        coeffs = np.polyfit(x, self.values, 1)
        return float(coeffs[0])

    def forecast(self, years_ahead=3, method='moving_average'):
        """Return a DataFrame with year + forecast columns."""
        if method == 'exponential_smoothing':
            base = self.exponential_smoothing()
        else:
            base = self.moving_average()

        trend = self.linear_trend() * 0.3  # damped trend
        rows = []
        for i in range(1, years_ahead + 1):
            val = base + trend * i
            rows.append({
                'year': self.last_year + i,
                'forecast': round(val, 2),
            })
        return pd.DataFrame(rows)

    def get_risk_indicator(self):
        """Determine trend direction from recent values."""
        if len(self.values) < 3:
            return 'Insufficient Data'
        recent = self.values[-3:]
        if recent[-1] > recent[0]:
            return 'Improving'
        elif recent[-1] < recent[0]:
            return 'Declining'
        return 'Stable'


def forecast_all_metrics(df, years_ahead=3, method='moving_average'):
    """Forecast all key metrics from the yearly summary.

    Parameters
    ----------
    df : DataFrame with columns: year, placement_rate, higher_studies_rate,
         unplaced_rate, avg_package, median_package, num_recruiters
    years_ahead : int
    method : str

    Returns
    -------
    dict of {metric_name: DataFrame with year + forecast columns}
    """
    metrics_config = [
        ('placement_rate', 'Placement Rate (%)'),
        ('higher_studies_rate', 'Higher Studies Rate (%)'),
        ('unplaced_rate', 'Unplaced Rate (%)'),
        ('avg_package', 'Average Package (LPA)'),
        ('median_package', 'Median Package (LPA)'),
        ('num_recruiters', 'Number of Recruiters'),
    ]

    results = {}
    for col, display_name in metrics_config:
        if col not in df.columns:
            continue
        series = df.dropna(subset=[col])
        if series.empty:
            continue
        forecaster = PlacementForecaster(series['year'], series[col], display_name)
        forecast_df = forecaster.forecast(years_ahead, method)
        forecast_df['metric'] = display_name
        results[display_name] = {
            'forecast': forecast_df,
            'risk': forecaster.get_risk_indicator(),
            'last_value': float(series[col].iloc[-1]),
        }
    return results


def get_historical_and_forecast(df, col, years_ahead=3, method='moving_average'):
    """Combine historical data with forecast for charting.

    Returns
    -------
    historical_df, forecast_df  (both have 'year' and 'value' columns)
    """
    if col not in df.columns or 'year' not in df.columns:
        return pd.DataFrame(columns=['year', 'value']), pd.DataFrame(columns=['year', 'value'])

    series = df.dropna(subset=[col])
    historical = pd.DataFrame({'year': series['year'], 'value': series[col]})

    if series.empty:
        return historical, pd.DataFrame(columns=['year', 'value'])

    forecaster = PlacementForecaster(series['year'], series[col])
    forecast = forecaster.forecast(years_ahead, method)
    forecast = forecast.rename(columns={'forecast': 'value'})

    return historical, forecast
