from django.db import models
from django.utils import timezone
from lease_rental_management.models import PropertyManager
from core.models import Property, Report, TimeStampedModel


class PortfolioDashboard(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    dashboard_name = models.CharField(max_length=255, blank=True, null=True)
    display_metrics = models.JSONField(default=list, blank=True, null=True)
    customizations = models.JSONField(default=dict, blank=True, null=True)
    thresholds = models.JSONField(default=dict, blank=True, null=True)

    def create_dashboard(self, property_manager_id, dashboard_name, display_metrics, customizations, thresholds):
        self.property_manager = property_manager_id
        self.dashboard_name = dashboard_name
        self.display_metrics = display_metrics
        self.customizations = customizations
        self.thresholds = thresholds
        self.save()

    def update_dashboard(self, display_metrics=None, customizations=None, thresholds=None):
        if display_metrics is not None:
            self.display_metrics = display_metrics
        if customizations is not None:
            self.customizations = customizations
        if thresholds is not None:
            self.thresholds = thresholds
        self.save()

    def delete_dashboard(self):
        self.delete()

    def get_dashboard(self):
        return {
            "id": self.id,
            "property_manager": self.property_manager.user_id,
            "dashboard_name": self.dashboard_name,
            "display_metrics": self.display_metrics,
            "customizations": self.customizations,
            "thresholds": self.thresholds
        }


class PropertyMetric(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    dashboard = models.ForeignKey(PortfolioDashboard, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=255, blank=True, null=True)
    metric_type = models.CharField(max_length=50, blank=True, null=True)
    metric_value = models.FloatField(blank=True, null=True)

    def create_metric(self, dashboard_id, metric_name, metric_type, metric_value):
        self.dashboard = dashboard_id
        self.metric_name = metric_name
        self.metric_type = metric_type
        self.metric_value = metric_value
        self.save()

    def update_metric(self, metric_value=None):
        if metric_value is not None:
            self.metric_value = metric_value
        self.save()

    def delete_metric(self):
        self.delete()

    def get_metric(self):
        return {
            "id": self.id,
            "dashboard_id": self.dashboard.id,
            "metric_name": self.metric_name,
            "metric_type": self.metric_type,
            "metric_value": self.metric_value,
        }


class PropertyReport(Report):
    dashboard = models.ForeignKey(PortfolioDashboard, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    report_date = models.DateField(default=timezone.now, blank=True, null=True)

    def create_report(self, title, data, dashboard, property_id, report_date):
        self.title = title
        self.data = data
        self.dashboard = dashboard
        self.property = property_id
        self.report_date = report_date
        self.save()

    def update_report(self, report_date=None):
        if report_date is not None:
            self.report_date = report_date
        self.save()

    def delete_report(self):
        self.delete()

    def get_report(self):
        return {
            "id": self.report_id,
            "title": self.title,
            "data": self.data,
            "dashboard_id": self.dashboard.id,
            "property_id": self.property.property_id,
            "report_date": self.report_date
        }


class ForecastingModel(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    dashboard = models.ForeignKey(PortfolioDashboard, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255, blank=True, null=True)
    model_type = models.CharField(max_length=50, blank=True, null=True)
    model_parameters = models.JSONField(default=dict, blank=True, null=True)
    forecast_results = models.JSONField(default=dict, blank=True, null=True)

    def create_model(self, dashboard, model_name, model_type, model_parameters, forecast_results):
        self.dashboard = dashboard
        self.model_name = model_name
        self.model_type = model_type
        self.model_parameters = model_parameters
        self.forecast_results = forecast_results
        self.save()

    def update_model(self, model_parameters=None, forecast_results=None):
        if model_parameters is not None:
            self.model_parameters = model_parameters
        if forecast_results is not None:
            self.forecast_results = forecast_results
        self.save()

    def delete_model(self):
        self.delete()

    def get_model(self):
        return {
            "id": self.id,
            "dashboard_id": self.dashboard.id,
            "model_name": self.model_name,
            "model_type": self.model_type,
            "model_parameters": self.model_parameters,
            "forecast_results": self.forecast_results
        }
