from django.db import models
from core.models import Report
from property_listing.models import PropertyOwner, RealEstateAgent
from lease_rental_management.models import PropertyManager


class CustomizableFinancialReport(Report):
    property_owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    filters = models.CharField(max_length=100, choices=[('property', 'Property'), ('timeframe', 'Timeframe')], default='property')
    groupings = models.JSONField(blank=True, null=True)
    sort_options = models.JSONField(blank=True, null=True)

    def build_report(self, fields, filters, groupings, sort_options):
        report_data = {
            "fields": fields,
            "filters": filters,
            "groupings": groupings,
            "sort_options": sort_options,
        }
        return report_data

    def export_report(self, format):
        export_data = f"Exporting report in {format} format."
        return export_data

    def generate_summary(self):
        summary = f"Summary for report owned by {self.property_owner.username}"
        return summary

    def apply_filters(self, filters):
        self.filters = filters
        self.save()
        return f"Filters applied: {filters}"


class SalesReport(Report):
    real_estate_agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    template = models.TextField(blank=True, null=True)
    fields = models.CharField(max_length=100, choices=[('listings', 'Listings'), ('leads', 'Leads'), (' transactions', ' Transactions')], default='listings')
    filters = models.CharField(max_length=100, choices=[('listing', 'Listing'), ('timeframe', 'Timeframe')], default='listing')
    visualizations = models.JSONField(blank=True, null=True)

    def create_report_from_template(self, template, fields, filters, visualizations):
        report_content = {
            "template": template,
            "fields": fields,
            "filters": filters,
            "visualizations": visualizations,
        }
        return report_content

    def modify_template(self, fields, filters, visualizations):
        self.fields = fields
        self.filters = filters
        self.visualizations = visualizations
        self.save()
        return f"Template modified with new fields: {fields}, filters: {filters}, and visualizations: {visualizations}"

    def schedule_report(self, schedule):
        return f"Report scheduled for {schedule}"

    def send_report(self, recipients):
        return f"Report sent to {recipients}"


class MaintenanceReport(Report):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    fields = models.CharField(max_length=100, choices=[('service_requests', 'Service Requests'), ('work_orders', 'Work Orders'), (' vendor_performance', 'Vendor Performance')], default='listings')
    filters = models.CharField(max_length=100, choices=[('location', 'Location'), ('category', 'Category'), ('urgency', 'Urgency')], default='location')
    dashboard = models.JSONField(blank=True, null=True)

    def generate_report(self, fields, filters):
        report_data = {
            "fields": fields,
            "filters": filters,
        }
        return report_data

    def view_dashboard(self):
        return self.dashboard

    def drill_down(self, criteria):
        drill_down_data = f"Drill down data based on criteria: {criteria}"
        return drill_down_data

    def update_status(self, status):
        self.dashboard['status'] = status
        self.save()
        return f"Status updated to: {status}"


class InvestmentReport(Report):
    fields = models.CharField(max_length=100, choices=[('property_performance', 'Property Performance'), ('market_trends', 'Market Trends'), (' investment_metrics', 'Investment Metrics')], default='property_performance')
    filters = models.CharField(max_length=100, choices=[('property', 'Property'), ('market', 'Market'), ('metrics', 'Metrics')], default='property')
    external_data_sources = models.JSONField(blank=True, null=True)

    def analyze_investment(self, fields, filters):
        analysis_result = {
            "fields": fields,
            "filters": filters,
        }
        return analysis_result

    def compare_market_data(self, external_data_sources):
        comparison = f"Comparing internal data with: {external_data_sources}"
        return comparison

    def generate_investment_summary(self):
        summary = f"Investment summary generated with filters: {self.filters}"
        return summary

    def apply_benchmarks(self, benchmarks):
        benchmark_result = f"Benchmarks applied: {benchmarks}"
        return benchmark_result


class ComplianceReport(Report):
    template = models.TextField(blank=True, null=True)
    fields = models.CharField(max_length=100, choices=[('regulatory_requirements', 'Regulatory Requirements'), ('audit findings', 'Audit Findings'), (' compliance_status', 'Compliance Status')], default='regulatory_requirements')
    filters = models.CharField(max_length=100, choices=[('regulation', 'Regulation'), ('property', 'Property')], default='property')

    def create_compliance_report(self, template, fields, filters):
        report_data = {
            "template": template,
            "fields": fields,
            "filters": filters,
        }
        return report_data

    def track_audit_trails(self):
        audit_trails = f"Audit trails tracked for report: {self.report_id}"
        return audit_trails

    def manage_documentation(self):
        documentation = f"Documentation managed for report: {self.report_id}"
        return documentation

    def generate_compliance_summary(self):
        summary = f"Compliance summary generated with filters: {self.filters}"
        return summary

