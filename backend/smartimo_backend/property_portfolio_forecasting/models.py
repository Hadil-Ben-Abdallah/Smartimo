from django.db import models
from lease_rental_management.models import PropertyManager
import json

class HistoricalDataAnalyzer(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    historical_data = models.JSONField(blank=True, null=True)
    demographic_factors = models.JSONField(blank=True, null=True)
    visualization_tools = models.JSONField(blank=True, null=True)

    def analyze_data(self):
        analysis_results = {}
        for data_point in self.historical_data:
            if 'rental_rate' in data_point and 'demographic_growth' in self.demographic_factors:
                analysis_results[data_point['year']] = {
                    'correlation': data_point['rental_rate'] * self.demographic_factors[data_point['year']]['growth_rate']
                }
        return analysis_results

    def generate_visualizations(self):
        visualizations = {
            "type": "bar_chart",
            "data": [
                {"year": data_point['year'], "value": data_point['rental_rate']}
                for data_point in self.historical_data
            ]
        }
        self.visualization_tools = json.dumps(visualizations)
        return self.visualization_tools

    def apply_regression_models(self):
        regression_results = []
        for data_point in self.historical_data:
            regression_results.append({
                "year": data_point['year'],
                "predicted_value": data_point['rental_rate'] * 1.05
            })
        return regression_results


class DemandForecaster(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    predictive_model = models.JSONField(blank=True, null=True)
    input_parameters = models.JSONField(blank=True, null=True)
    forecast_results = models.JSONField(blank=True, null=True)

    def forecast_demand(self):
        forecast = {}
        for param in self.input_parameters:
            forecast[param['region']] = param['population_growth'] * self.predictive_model.get('base_demand', 1)
        self.forecast_results = json.dumps(forecast)
        return self.forecast_results

    def customize_forecast(self, custom_parameters):
        customized_forecast = {}
        for param in custom_parameters:
            customized_forecast[param['region']] = param['population_growth'] * self.predictive_model.get('base_demand', 1)
        self.forecast_results = json.dumps(customized_forecast)
        return self.forecast_results

    def visualize_forecast(self):
        visualizations = {
            "type": "line_chart",
            "data": [
                {"region": region, "forecast": value}
                for region, value in json.loads(self.forecast_results).items()
            ]
        }
        return visualizations


class RentalIncomePredictor(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    income_model = models.JSONField(blank=True, null=True)
    rental_data = models.JSONField(blank=True, null=True)
    projection_scenarios = models.JSONField(blank=True, null=True)
    cash_flow_projections = models.JSONField(blank=True, null=True)

    def predict_rental_income(self):
        income_projection = {}
        for data in self.rental_data:
            income_projection[data['year']] = data['rental_rate'] * data['occupancy_rate']
        self.cash_flow_projections = json.dumps(income_projection)
        return self.cash_flow_projections

    def simulate_scenarios(self, scenario_parameters):
        scenario_results = {}
        for scenario in scenario_parameters:
            scenario_results[scenario['year']] = scenario['rental_rate'] * scenario['occupancy_rate'] * (1 + scenario.get('rent_increase', 0))
        self.projection_scenarios = json.dumps(scenario_results)
        return self.projection_scenarios

    def generate_cash_flow_report(self):
        report = {
            "summary": "Cash Flow Projections",
            "data": json.loads(self.cash_flow_projections)
        }
        return report


class MarketTrendAnalyzer(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    market_data = models.JSONField(blank=True, null=True)
    trend_analysis_tools = models.JSONField(blank=True, null=True)
    investment_opportunities = models.JSONField(blank=True, null=True)

    def analyze_market_trends(self):
        trends = {}
        for data in self.market_data:
            if 'growth_rate' in data:
                trends[data['property_type']] = data['growth_rate']
        self.trend_analysis_tools = json.dumps(trends)
        return self.trend_analysis_tools

    def generate_heat_maps(self):
        heat_map = {
            "type": "heat_map",
            "data": [
                {"location": data['location'], "score": data['investment_score']}
                for data in self.market_data
            ]
        }
        return heat_map

    def prioritize_opportunities(self):
        opportunities = sorted(
            json.loads(self.investment_opportunities),
            key=lambda x: x['investment_score'], reverse=True
        )
        return opportunities


class InvestmentScenarioEvaluator(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    scenario_models = models.JSONField(blank=True, null=True)
    input_parameters = models.JSONField(blank=True, null=True)
    scenario_results = models.JSONField(blank=True, null=True)

    def evaluate_investment_scenarios(self):
        results = {}
        for scenario in self.input_parameters:
            results[scenario['scenario_name']] = {
                "expected_return": scenario['investment_cost'] * scenario['expected_return_rate']
            }
        self.scenario_results = json.dumps(results)
        return self.scenario_results

    def compare_scenarios(self):
        comparison = []
        for scenario in json.loads(self.scenario_results):
            comparison.append({
                "scenario": scenario,
                "expected_return": json.loads(self.scenario_results)[scenario]["expected_return"]
            })
        return comparison

    def prioritize_investment_strategies(self):
        strategies = sorted(
            json.loads(self.scenario_results),
            key=lambda x: x['expected_return'], reverse=True
        )
        return strategies

