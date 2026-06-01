import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

class SimpleForecaster:
    """Simple forecasting using Moving Average and Exponential Smoothing"""
    
    def __init__(self, data_series, name="Metric"):
        self.data = data_series.values
        self.years = data_series.index.values
        self.name = name
        self.last_year = int(self.years[-1])
    
    def moving_average(self, window=3):
        """Simple Moving Average forecast"""
        if len(self.data) < window:
            window = len(self.data) // 2
        
        forecast_value = np.mean(self.data[-window:])
        return forecast_value
    
    def exponential_smoothing(self, alpha=0.3):
        """Exponential Smoothing forecast"""
        forecast = self.data[0]
        for value in self.data[1:]:
            forecast = alpha * value + (1 - alpha) * forecast
        return forecast
    
    def forecast_next_year(self, method='moving_average'):
        """Get forecast for next year"""
        if method == 'moving_average':
            return self.moving_average()
        elif method == 'exponential_smoothing':
            return self.exponential_smoothing()
        else:
            return np.mean(self.data)
    
    def get_multiple_year_forecast(self, years_ahead=3, method='moving_average'):
        """Forecast multiple years ahead"""
        forecasts = []
        
        if method == 'moving_average':
            base_forecast = self.moving_average()
            trend = (self.data[-1] - self.data[-3]) / 2 if len(self.data) >= 3 else 0
        else:
            base_forecast = self.exponential_smoothing()
            trend = (self.data[-1] - self.data[-2]) if len(self.data) >= 2 else 0
        
        for year in range(years_ahead):
            # Simple trend extrapolation
            forecast_value = base_forecast + (trend * year * 0.1)
            forecasts.append({
                'year': self.last_year + year + 1,
                'forecast': round(forecast_value, 2),
                'method': method
            })
        
        return pd.DataFrame(forecasts)

def forecast_all_metrics(df_yearly, years_ahead=3):
    """Forecast all key metrics"""
    
    metrics_to_forecast = [
        ('placement_rate_pct', 'Placement Rate (%)'),
        ('higher_studies_rate_pct', 'Higher Studies Rate (%)'),
        ('unplaced_rate_pct', 'Unplaced Rate (%)'),
        ('median_package_lpa', 'Median Package (LPA)'),
        ('average_package_lpa', 'Average Package (LPA)')
    ]
    
    forecasts_dict = {}
    
    for col, display_name in metrics_to_forecast:
        data_series = df_yearly.set_index('graduation_year')[col]
        
        # Use Moving Average as default
        forecaster = SimpleForecaster(data_series, display_name)
        forecast_df = forecaster.get_multiple_year_forecast(years_ahead=years_ahead, 
                                                             method='moving_average')
        forecasts_dict[display_name] = forecast_df
    
    return forecasts_dict

def get_forecast_comparison(df_yearly, metric='placement_rate_pct'):
    """Get historical + forecasted values for a specific metric"""
    
    data_series = df_yearly.set_index('graduation_year')[metric]
    forecaster = SimpleForecaster(data_series)
    
    # Get historical data
    historical = pd.DataFrame({
        'year': df_yearly['graduation_year'],
        'actual': df_yearly[metric],
        'type': 'Historical'
    })
    
    # Get forecast
    forecast_df = forecaster.get_multiple_year_forecast(years_ahead=3, 
                                                         method='moving_average')
    forecast_df.columns = ['year', 'actual', 'method']
    forecast_df['type'] = 'Forecasted'
    forecast_df = forecast_df.drop('method', axis=1)
    
    # Combine
    combined = pd.concat([historical, forecast_df], ignore_index=True)
    return combined
