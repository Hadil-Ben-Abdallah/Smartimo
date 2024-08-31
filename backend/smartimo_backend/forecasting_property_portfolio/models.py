from django.db import models
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from datetime import datetime
from core.models import Property

class HistoricalOccupancyData(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    occupancy_rate = models.FloatField(blank=True, null=True)
    time_period = models.CharField(max_length=100, choices=[('month', 'Month'), ('quarter', 'Quater'), ('year', 'Year')], default='month')
    market_trends = models.JSONField(blank=True, null=True)

    def aggregate_data(self, property_id, start_date, end_date):
        data = HistoricalOccupancyData.objects.filter(
            property=property_id, 
            time_period__range=[start_date, end_date]
        ).values('time_period', 'occupancy_rate', 'market_trends')
        return pd.DataFrame(list(data))

    def analyze_trends(self, data):
        data['time_period'] = pd.to_datetime(data['time_period'])
        data.set_index('time_period', inplace=True)
        result = data['occupancy_rate'].resample('M').mean().fillna(method='ffill').pct_change()
        return result

    def forecast_demand(self, data):
        model = ARIMA(data['occupancy_rate'], order=(5, 1, 0))
        fit = model.fit()
        forecast = fit.forecast(steps=12)
        return forecast

class MarketConditionAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    external_data_source = models.CharField(max_length=255, choices=[('real-time', 'Real Time'), ('market_data', 'Market Data'), ('economic_indicators', 'Economic Indicators')], default='real-time')
    investment_opportunities = models.JSONField(blank=True, null=True)
    risk_factors = models.JSONField(blank=True, null=True)

    def gather_market_data(self, property_id, data_source):
        data = pd.DataFrame({
            'date': pd.date_range(start='1/1/2020', periods=100),
            'market_index': np.random.rand(100)
        })
        return data

    def perform_regression_analysis(self, data):
        X = np.array(data.index).reshape(-1, 1)
        y = data['market_index'].values
        model = LinearRegression().fit(X, y)
        trend = model.predict(X)
        return trend

    def optimize_portfolio_allocation(self, data):
        allocations = {'Property A': 0.4, 'Property B': 0.6}
        return allocations

class RentalIncomeForecast(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    historical_rental_income = models.FloatField(blank=True, null=True)
    cash_flow_projections = models.JSONField(blank=True, null=True)
    expense_projections = models.JSONField(blank=True, null=True)

    def generate_income_projections(self, property_id, historical_data):
        data = pd.DataFrame(historical_data)
        model = LinearRegression().fit(data[['time_period']], data['historical_rental_income'])
        future_dates = pd.date_range(start=datetime.today(), periods=12, freq='M').to_julian_date()
        projections = model.predict(future_dates.reshape(-1, 1))
        return projections

    def calculate_cash_flow(self, rental_projections, expense_projections):
        cash_flow = np.array(rental_projections) - np.array(expense_projections)
        return cash_flow

    def update_projections(self, new_data):
        updated_projections = self.generate_income_projections(new_data['property_id'], new_data['historical_rental_income'])
        self.cash_flow_projections = updated_projections
        self.save()
        return self.cash_flow_projections

class PropertyValueForecast(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    historical_sales_data = models.JSONField(blank=True, null=True)
    appreciation_rate_forecast = models.FloatField(blank=True, null=True)
    time_series_forecast = models.JSONField(blank=True, null=True)

    def aggregate_sales_data(self, property_id):
        data = PropertyValueForecast.objects.filter(property=property_id).values('historical_sales_data')
        return pd.DataFrame(list(data))

    def forecast_appreciation_rate(self, sales_data):
        model = ARIMA(sales_data['price'], order=(1, 1, 0))
        fit = model.fit()
        forecast = fit.forecast(steps=12)
        return forecast

    def analyze_market_comparables(self, comparable_data):
        analysis = comparable_data.mean()
        return analysis

class EmergingMarketTrends(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    market_trends = models.JSONField(blank=True, null=True)
    economic_indicators = models.JSONField(blank=True, null=True)
    scenario_analysis = models.JSONField(blank=True, null=True)

    def monitor_trends(self, property_id):
        data = pd.DataFrame({
            'date': pd.date_range(start='1/1/2021', periods=100),
            'trend_index': np.random.rand(100)
        })
        return data

    def perform_scenario_analysis(self, trend_data):
        scenario_result = trend_data.describe()
        return scenario_result

    def recommend_portfolio_adjustments(self, analysis_result):
        adjustments = {'Property A': 'Sell', 'Property B': 'Hold'}
        return adjustments

class DemographicImpactAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    demographic_data = models.JSONField(blank=True, null=True)
    urbanization_trends = models.JSONField(blank=True, null=True)
    regulatory_changes = models.JSONField(blank=True, null=True)
    impact_forecast = models.JSONField(blank=True, null=True)

    def aggregate_demographic_data(self, property_id, data_source):
        data = pd.DataFrame({
            'year': pd.date_range(start='1/1/2010', periods=10, freq='A'),
            'population': np.random.randint(10000, 50000, size=10)
        })
        return data

    def forecast_market_impact(self, demographic_data):
        model = LinearRegression().fit(demographic_data[['year']], demographic_data['population'])
        future_years = pd.date_range(start=datetime.today(), periods=5, freq='A').to_julian_date()
        forecast = model.predict(future_years.reshape(-1, 1))
        return forecast

    def support_strategic_planning(self, impact_forecast):
        recommendations = {'Strategy A': 'Expand', 'Strategy B': 'Hold'}
        return recommendations
