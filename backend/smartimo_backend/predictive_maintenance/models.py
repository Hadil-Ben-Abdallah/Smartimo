from django.db import models
from core.models import Property, User, TimeStampedModel
from maintenance_and_service_requests.models import MaintenanceTechnician

class DataSource(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, choices=[('IoT_sensor', 'IoT Sensor'), ('building_management_system', 'Building Management System')], default='building_management_system')
    data = models.JSONField(blank=True, null=True)

    def update_data(self, data: dict):
        self.data = data
        self.save()

    def get_data(self):
        return self.data


class PredictionModel(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    algorithm = models.CharField(max_length=100, blank=True, null=True)
    parameters = models.JSONField(blank=True, null=True)
    training_data = models.JSONField(blank=True, null=True)

    def train(self, data: dict):
        self.training_data = data
        self.parameters = {"example_param": "updated_value"}  
        self.save()

    def predict(self, data: dict):
        prediction = {"example_output": "predicted_value"}
        return prediction

    def update_parameters(self, parameters: dict):
        self.parameters = parameters
        self.save()


class MaintenanceAlert(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    prediction = models.JSONField(blank=True, null=True)
    threshold = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')

    def update_status(self, status: str):
        self.status = status
        self.save()

    def get_details(self):
        return {
            "property": self.property.address,
            "prediction": self.prediction,
            "threshold": self.threshold,
            "status": self.status,
        }

    def notify_user(self, user_id: int):
        user = User.objects.get(id=user_id)
        notification = f"Alert: Maintenance needed for property {self.property.address}"
        return True


class PredictiveMaintenanceSystem(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    data_sources = models.ManyToManyField(DataSource, blank=True, null=True)
    models = models.ManyToManyField(PredictionModel, blank=True, null=True)
    alerts = models.ManyToManyField(MaintenanceAlert, blank=True, null=True)

    def integrate_data_source(self, data_source: DataSource):
        self.data_sources.add(data_source)
        self.save()

    def train_model(self, model: PredictionModel):
        historical_data = {}
        model.train(historical_data)
        self.models.add(model)
        self.save()

    def generate_alerts(self):
        pass

    def get_reports(self):
        reports = []
        for alert in self.alerts.all():
            reports.append(alert.get_details())
        return reports


class WorkOrder(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    alert = models.ForeignKey(MaintenanceAlert, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(MaintenanceTechnician, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('assigned', 'Assigned'), ('in-progress', 'In-Progress'), ('completed', 'Completed')], default='assigned')
    scheduled_date = models.DateField(blank=True, null=True)

    def update_status(self, status: str):
        self.status = status
        self.save()

    def assign_task(self, user_id: int):
        self.assigned_to = MaintenanceTechnician.objects.get(id=user_id)
        self.save()

    def schedule_work(self, date: str):
        self.scheduled_date = date
        self.save()


class MaintenancePerformanceMetric(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def record_metric(self, value: float):
        self.value = value
        self.save()

    def generate_report(self):
        report = {
            "property": self.property.address,
            "metric_name": self.metric_name,
            "value": self.value,
        }
        return report

    def analyze_trends(self):
        trends = {"example_trend": "trend_value"}
        return trends


class Integration(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    system_type = models.CharField(max_length=100, blank=True, null=True)
    api_endpoint = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')

    def connect_system(self, endpoint: str):
        self.api_endpoint = endpoint
        self.status = 'active'
        self.save()

    def sync_data(self):
        data_synced = True
        return data_synced

    def get_integration_status(self):
        return self.status

