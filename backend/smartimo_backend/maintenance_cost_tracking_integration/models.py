from django.db import models
from django.contrib.postgres.fields import JSONField
from core.models import Property, Report
from vendor_management.models import Vendor

class MaintenanceExpense(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    expense_date = models.DateField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    cost_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    custom_fields = JSONField(blank=True, null=True)

    def record_expense(self, property, expense_date, vendor, service_type, cost_amount, category, tags, custom_fields):
        self.property = property
        self.expense_date = expense_date
        self.vendor = vendor
        self.service_type = service_type
        self.cost_amount = cost_amount
        self.category = category
        self.tags = tags
        self.custom_fields = custom_fields
        self.save()

    def update_expense(self, expense_date=None, vendor=None, service_type=None, cost_amount=None, category=None, tags=None, custom_fields=None):
        if expense_date:
            self.expense_date = expense_date
        if vendor:
            self.vendor = vendor
        if service_type:
            self.service_type = service_type
        if cost_amount:
            self.cost_amount = cost_amount
        if category:
            self.category = category
        if tags:
            self.tags = tags
        if custom_fields:
            self.custom_fields = custom_fields
        self.save()

    def categorize_expense(self, category, tags):
        self.category = category
        self.tags = tags
        self.save()

    def get_expense_details(self):
        return {
            'id': self.id,
            'property': self.property.property_id,
            'expense_date': self.expense_date,
            'vendor': self.vendor.id,
            'service_type': self.service_type,
            'cost_amount': str(self.cost_amount),
            'category': self.category,
            'tags': self.tags,
            'custom_fields': self.custom_fields
        }

class RecurringMaintenanceRule(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.CharField(max_length=255, blank=True, null=True)
    cost_threshold = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vendor_contract = models.CharField(max_length=255, blank=True, null=True)
    automation_rules = JSONField(blank=True, null=True)

    def create_rule(self, property, maintenance_type, frequency, cost_threshold, vendor_contract, automation_rules):
        self.property = property
        self.maintenance_type = maintenance_type
        self.frequency = frequency
        self.cost_threshold = cost_threshold
        self.vendor_contract = vendor_contract
        self.automation_rules = automation_rules
        self.save()

    def update_rule(self, maintenance_type=None, frequency=None, cost_threshold=None, vendor_contract=None, automation_rules=None):
        if maintenance_type:
            self.maintenance_type = maintenance_type
        if frequency:
            self.frequency = frequency
        if cost_threshold:
            self.cost_threshold = cost_threshold
        if vendor_contract:
            self.vendor_contract = vendor_contract
        if automation_rules:
            self.automation_rules = automation_rules
        self.save()

    def apply_rule(self):
        pass

    def get_rule_details(self):
        return {
            'id': self.id,
            'property': self.property.property_id,
            'maintenance_type': self.maintenance_type,
            'frequency': self.frequency,
            'cost_threshold': str(self.cost_threshold),
            'vendor_contract': self.vendor_contract,
            'automation_rules': self.automation_rules
        }

class MaintenanceCostReport(Report):
    report_date = models.DateField(blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    average_cost_per_property = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_breakdown = JSONField(blank=True, null=True)
    custom_filters = JSONField(blank=True, null=True)

    def generate_report(self, property, report_date, total_expenses, average_cost_per_property, cost_breakdown, custom_filters):
        self.property = property
        self.report_date = report_date
        self.total_expenses = total_expenses
        self.average_cost_per_property = average_cost_per_property
        self.cost_breakdown = cost_breakdown
        self.custom_filters = custom_filters
        self.save()

    def filter_report(self, custom_filters):
        self.custom_filters = custom_filters
        self.save()

    def get_report_details(self):
        return {
            'id': self.report_id,
            'report_date': self.report_date,
            'property': self.property.property_id,
            'total_expenses': str(self.total_expenses),
            'average_cost_per_property': str(self.average_cost_per_property),
            'cost_breakdown': self.cost_breakdown,
            'custom_filters': self.custom_filters
        }

class MaintenanceBudget(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    budget_target = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expense_threshold = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    allocation_limits = JSONField(blank=True, null=True)
    variance_tolerances = JSONField(blank=True, null=True)

    def set_budget(self, property, budget_target, expense_threshold, allocation_limits, variance_tolerances):
        self.property = property
        self.budget_target = budget_target
        self.expense_threshold = expense_threshold
        self.allocation_limits = allocation_limits
        self.variance_tolerances = variance_tolerances
        self.save()

    def update_budget(self, budget_target=None, expense_threshold=None, allocation_limits=None, variance_tolerances=None):
        if budget_target:
            self.budget_target = budget_target
        if expense_threshold:
            self.expense_threshold = expense_threshold
        if allocation_limits:
            self.allocation_limits = allocation_limits
        if variance_tolerances:
            self.variance_tolerances = variance_tolerances
        self.save()

    def track_expenses(self):
        pass

    def get_budget_details(self):
        return {
            'id': self.id,
            'property': self.property.property_id,
            'budget_target': str(self.budget_target),
            'expense_threshold': str(self.expense_threshold),
            'allocation_limits': self.allocation_limits,
            'variance_tolerances': self.variance_tolerances
        }

class FinancialIntegration(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    system_type = models.CharField(max_length=255, blank=True, null=True)
    integration_settings = JSONField(blank=True, null=True)
    data_format = models.CharField(max_length=255, blank=True, null=True)
    sync_status = models.CharField(max_length=255, blank=True, null=True)

    def setup_integration(self, property, system_type, integration_settings, data_format):
        self.property = property
        self.system_type = system_type
        self.integration_settings = integration_settings
        self.data_format = data_format
        self.save()

    def update_integration(self, system_type=None, integration_settings=None, data_format=None):
        if system_type:
            self.system_type = system_type
        if integration_settings:
            self.integration_settings = integration_settings
        if data_format:
            self.data_format = data_format
        self.save()

    def export_data(self):
        pass

    def sync_data(self):
        pass

    def get_integration_status(self):
        return {
            'id': self.id,
            'property_id': self.property.property_id,
            'system_type': self.system_type,
            'integration_settings': self.integration_settings,
            'data_format': self.data_format,
            'sync_status': self.sync_status
        }

