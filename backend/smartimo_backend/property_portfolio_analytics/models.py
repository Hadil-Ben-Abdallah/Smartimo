from django.db import models
from core.models import Report
from lease_rental_management.models import PropertyManager

class PropertyPortfolioDashboard(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    kpi_widgets = models.JSONField(default=dict, blank=True, null=True)
    real_time_updates = models.BooleanField(default=True, blank=True, null=True)
    customization_settings = models.JSONField(default=dict, blank=True, null=True)

    def configure_dashboard(self, kpi_widgets, customization_settings):
        self.kpi_widgets = kpi_widgets
        self.customization_settings = customization_settings
        self.save()

    def add_kpi_widget(self, widget_name, widget_data):
        self.kpi_widgets[widget_name] = widget_data
        self.save()

    def update_dashboard(self, kpi_data):
        for widget_name, widget_value in kpi_data.items():
            if widget_name in self.kpi_widgets:
                self.kpi_widgets[widget_name].update(widget_value)
        self.save()

    def remove_kpi_widget(self, widget_name):
        if widget_name in self.kpi_widgets:
            del self.kpi_widgets[widget_name]
            self.save()


class PortfolioPerformanceReport(Report):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    report_template = models.TextField(blank=True, null=True)
    occupancy_rates = models.JSONField(default=dict, blank=True, null=True)
    rental_income = models.JSONField(default=dict, blank=True, null=True)
    expenses = models.JSONField(default=dict, blank=True, null=True)
    net_operating_income = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    financial_returns = models.JSONField(default=dict)
    export_format = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('csv', 'CSV')], default='pdf')

    def generate_report(self):
        self.net_operating_income = sum(self.rental_income.values()) - sum(self.expenses.values())
        self.save()

    def export_report(self):
        if self.export_format == 'pdf':
            return f"Report exported as {self.id}.pdf"
        elif self.export_format == 'csv':
            return f"Report exported as {self.id}.csv"

    def customize_report(self, template, export_format):
        self.report_template = template
        self.export_format = export_format
        self.save()


class OccupancyAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    occupancy_data = models.JSONField(default=dict, blank=True, null=True)
    occupancy_trends = models.JSONField(default=dict, blank=True, null=True)
    alerts = models.JSONField(default=dict, blank=True, null=True)

    def track_occupancy_rates(self, property_id, occupancy_rate):
        self.occupancy_data[property_id] = occupancy_rate
        self.save()

    def analyze_occupancy_trends(self):
        self.occupancy_trends = {
            property_id: sum(rates) / len(rates) for property_id, rates in self.occupancy_data.items()
        }
        self.save()

    def generate_alerts(self, threshold=50):
        self.alerts = {
            property_id: rate for property_id, rate in self.occupancy_data.items() if rate < threshold
        }
        self.save()


class FinancialAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    rental_yield_data = models.JSONField(default=dict, blank=True, null=True)
    revenue_growth_data = models.JSONField(default=dict, blank=True, null=True)
    comparison_data = models.JSONField(default=dict, blank=True, null=True)
    financial_visualizations = models.JSONField(default=dict, blank=True, null=True)

    def calculate_rental_yields(self, property_id, rental_income, expenses):
        yield_value = (rental_income - expenses) / expenses if expenses != 0 else 0
        self.rental_yield_data[property_id] = yield_value
        self.save()

    def analyze_revenue_growth(self, property_id, revenue_data):
        self.revenue_growth_data[property_id] = revenue_data
        self.save()

    def generate_financial_visualizations(self):
        self.financial_visualizations = {
            "rental_yield_chart": "chart_data_here",
            "revenue_growth_chart": "chart_data_here"
        }
        self.save()


class ScenarioAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    market_conditions = models.JSONField(default=dict, blank=True, null=True)
    investment_scenarios = models.JSONField(default=dict, blank=True, null=True)
    scenario_forecasts = models.JSONField(default=dict, blank=True, null=True)
    sensitivity_analysis = models.JSONField(default=dict, blank=True, null=True)

    def run_scenario_analysis(self):
        self.scenario_forecasts = {
            "scenario_1": "forecast_data_here",
            "scenario_2": "forecast_data_here"
        }
        self.save()

    def adjust_parameters(self, new_market_conditions, new_investment_scenarios):
        self.market_conditions.update(new_market_conditions)
        self.investment_scenarios.update(new_investment_scenarios)
        self.save()

    def generate_scenario_forecasts(self):
        self.sensitivity_analysis = {
            "high_rent": "impact_data_here",
            "low_rent": "impact_data_here"
        }
        self.save()

