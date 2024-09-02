from django.db import models
from core.models import Property, Report, User, TimeStampedModel
from property_listing.models import PropertyOwner
from vendor_management.models import Vendor


class Portfolio(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def add_property(self, property: Property):
        self.properties.add(property)
        self.save()

    def remove_property(self, property: Property):
        self.properties.remove(property)
        self.save()

    def view_properties(self):
        return self.properties.all()

    def calculate_total_value(self):
        total_value = sum(property.value for property in self.properties.all())
        return total_value

    def update_description(self, new_description: str):
        self.description = new_description
        self.save()

class DashboardWidget(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    widget_type = models.CharField(max_length=100, choices=[('kpi', 'KPI'), ('chart', 'Chart'), ('report', 'Report')], default='kpi')
    data_source = models.CharField(max_length=255, blank=True, null=True)
    settings = models.JSONField(blank=True, null=True)

    def render_widget(self):
        return f"Rendering widget: {self.widget_type} with settings {self.settings}"

    def customize_widget(self, new_settings: dict):
        self.settings.update(new_settings)
        self.save()

class Dashboard(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    widgets = models.ManyToManyField(DashboardWidget)
    customizations = models.JSONField(blank=True, null=True)

    def load_dashboard(self):
        return {
            "widgets": [widget.render_widget() for widget in self.widgets.all()],
            "customizations": self.customizations
        }

    def update_widget(self, widget_id: int, new_settings: dict):
        widget = DashboardWidget.objects.get(widget_id=widget_id)
        widget.customize_widget(new_settings)
        self.save()

    def drill_down(self, entity_id: int, entity_type: str):
        if entity_type == "property":
            return Property.objects.get(property_id=entity_id)
        elif entity_type == "portfolio":
            return Portfolio.objects.get(portfolio_id=entity_id)
        return None

class PortfolioFinancialReport(Report):
    id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100, choices=[('income_statement', 'Income Statement'), ('balance_sheet', 'Balance Sheet')], default='income_statement')

    def generate_report(self):
        return f"Generating {self.report_type} for Portfolio ID {self.id}"

    def view_trends(self):
        return "Viewing trends for the financial report"

    def drill_down_details(self):
        return f"Drilling down details for Portfolio ID {self.id}"

class OperationalTask(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=[('pending', 'Pending'), ('in-progress', 'In-Progress'), ('completed', 'Completed')], default='pending')
    description = models.TextField(blank=True, null=True)

    def assign_task(self, vendor):
        self.assigned_to = vendor
        self.save()

    def update_task_status(self, new_status: str):
        self.status = new_status
        self.save()

    def track_performance(self):
        return f"Tracking performance for Vendor ID {self.assigned_to.id}"

class PortfolioAnalysis(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    parameters = models.JSONField(blank=True, null=True)
    results = models.JSONField(blank=True, null=True)

    def run_simulation(self):
        return f"Running simulation for Portfolio ID {self.portfolio.id}"

    def compare_scenarios(self):
        return "Comparing scenarios for the portfolio analysis"

    def generate_recommendations(self):
        return "Generating recommendations based on analysis"

class ReportGeneration(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    distribution_list = models.JSONField(blank=True, null=True)

    def create_report(self):
        return f"Creating report with ID {self.id}"

    def schedule_distribution(self, schedule_time: str):
        return f"Scheduling distribution for report ID {self.id} at {schedule_time}"

    def add_customizations(self, customizations: dict):
        return f"Adding customizations to report ID {self.id}"

