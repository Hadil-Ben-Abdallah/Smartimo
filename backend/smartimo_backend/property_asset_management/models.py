from django.db import models
from django.utils import timezone
from core.models import Property, User
from lease_rental_management.models import PropertyManager
from maintenance_and_service_requests.models import MaintenanceTechnician

class PropertyAsset(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, unique=True, blank=True, null=True)
    acquisition_date = models.DateTimeField(default=timezone.now)
    assigned_to = models.ForeignKey(PropertyManager, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, choices=[('active', 'Active'), ('in_maintenance', 'In Maintenance'), ('retired', 'Retired')],default="active")
    
    def catalog_asset(self, property_id, asset_type, location, model, serial_number, acquisition_date):
        self.property = property_id
        self.asset_type = asset_type
        self.location = location
        self.model = model
        self.serial_number = serial_number
        self.acquisition_date = acquisition_date
        self.status = "active"
        self.save()
    
    def edit_asset(self, updated_details):
        for key, value in updated_details.items():
            setattr(self, key, value)
        self.save()
    
    def remove_asset(self):
        self.delete()
    
    def assign_asset(self, assigned_to):
        self.assigned_to = assigned_to
        self.save()
    
    def get_asset_details(self):
        return {
            "id": self.id,
            "property": self.property,
            "asset_type": self.asset_type,
            "location": self.location,
            "model": self.model,
            "serial_number": self.serial_number,
            "acquisition_date": self.acquisition_date,
            "assigned_to": self.assigned_to,
            "status": self.status,
        }


class MaintenanceTeam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    members = models.ManyToManyField(MaintenanceTechnician, blank=True, null=True)

    def add_member(self, user):
        self.members.add(user)
    
    def remove_member(self, user):
        self.members.remove(user)
    
    def get_team(self):
        return {
            "team_id": self.id,
            "name": self.name,
            "contact_info": self.contact_info,
            "members": list(self.members.all()),
        }


class AssetAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(PropertyAsset, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(MaintenanceTeam, on_delete=models.CASCADE)
    permissions = models.JSONField(default=dict, blank=True, null=True)
    notification_settings = models.JSONField(default=dict, blank=True, null=True)
    
    def create_assignment(self, asset_id, assigned_to, permissions):
        self.asset = asset_id
        self.assigned_to = assigned_to
        self.permissions = permissions
        self.save()
    
    def update_assignment(self, updated_details):
        for key, value in updated_details.items():
            setattr(self, key, value)
        self.save()
    
    def get_assignment_details(self):
        return {
            "id": self.id,
            "asset": self.asset,
            "assigned_to": self.assigned_to,
            "permissions": self.permissions,
            "notification_settings": self.notification_settings,
        }


class MaintenanceSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(PropertyAsset, on_delete=models.CASCADE)
    task = models.CharField(max_length=255, blank=True, null=True)
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=[('scheduled', 'Scheduled'), (' in_progress', ' In Progress'), ('completed', 'Completed')],default="scheduled")
    completion_notes = models.TextField(blank=True, null=True)
    
    def schedule_maintenance(self, asset_id, task, assigned_technician, priority, due_date):
        self.asset = asset_id
        self.task = task
        self.assigned_technician = assigned_technician
        self.priority = priority
        self.due_date = due_date
        self.save()
    
    def update_task_status(self, status, completion_notes):
        self.status = status
        self.completion_notes = completion_notes
        self.save()
    
    def get_maintenance_history(self, asset_id):
        return MaintenanceSchedule.objects.filter(asset=asset_id).values()


class DepreciationTracker(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(PropertyAsset, on_delete=models.CASCADE)
    depreciation_method = models.CharField(max_length=255, choices=[('straight_line', 'Straight-Line'), ('accelerated', 'Accelerated')], default='straight_line')
    depreciation_rate = models.FloatField(blank=True, null=True)
    accumulated_depreciation = models.FloatField(default=0, blank=True, null=True)
    current_value = models.FloatField(blank=True, null=True)
    
    def calculate_depreciation(self):
        if self.depreciation_method == "straight_line":
            annual_depreciation = self.current_value * self.depreciation_rate
            self.accumulated_depreciation += annual_depreciation
            self.current_value -= annual_depreciation
        elif self.depreciation_method == "accelerated":
            pass
        self.save()
    
    def generate_depreciation_report(self):
        return {
            "asset": self.asset,
            "depreciation_method": self.depreciation_method,
            "depreciation_rate": self.depreciation_rate,
            "accumulated_depreciation": self.accumulated_depreciation,
            "current_value": self.current_value,
        }
    
    def update_depreciation_values(self, new_values):
        for key, value in new_values.items():
            setattr(self, key, value)
        self.save()


class AssetPerformance(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(PropertyAsset, on_delete=models.CASCADE)
    utilization_rate = models.FloatField(blank=True, null=True)
    downtime = models.FloatField(blank=True, null=True)
    maintenance_costs = models.FloatField(blank=True, null=True)
    lifecycle_stage = models.CharField(max_length=255, choices=[('new', 'New'), ('mid_life', 'Mid Life'), ('end_of_life', 'End Of Life')], default='new')
    
    def track_utilization(self, utilization_rate):
        self.utilization_rate = utilization_rate
        self.save()
    
    def record_downtime(self, downtime):
        self.downtime = downtime
        self.save()
    
    def log_maintenance_costs(self, costs):
        self.maintenance_costs += costs
        self.save()
    
    def analyze_performance(self):
        return {
            "utilization_rate": self.utilization_rate,
            "downtime": self.downtime,
            "maintenance_costs": self.maintenance_costs,
            "lifecycle_stage": self.lifecycle_stage,
        }


class AssetAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    asset_data = models.JSONField(default=dict, blank=True, null=True)
    optimization_recommendations = models.JSONField(default=dict, blank=True, null=True)
    
    def aggregate_asset_data(self, property_id):
        assets = PropertyAsset.objects.filter(property=property_id)
        data = []
        for asset in assets:
            data.append({
                "asset_type": asset.asset_type,
                "status": asset.status,
                "utilization_rate": asset.assetperformance.utilization_rate,
                "downtime": asset.assetperformance.downtime,
                "maintenance_costs": asset.assetperformance.maintenance_costs,
                "lifecycle_stage": asset.assetperformance.lifecycle_stage,
            })
        self.asset_data = data
        self.save()
    
    def generate_performance_reports(self, property_id):
        assets = PropertyAsset.objects.filter(property=property_id)
        reports = []
        for asset in assets:
            reports.append({
                "asset": asset.get_asset_details(),
                "performance": asset.assetperformance.analyze_performance(),
            })
        return reports
    
    def forecast_maintenance_needs(self, property_id):
        assets = PropertyAsset.objects.filter(property=property_id)
        forecasts = []
        for asset in assets:
            if asset.assetperformance.utilization_rate > 80:
                forecasts.append({
                    "asset": asset.get_asset_details(),
                    "forecast": "High maintenance need expected",
                })
        return forecasts
    
    def provide_optimization_recommendations(self, property_id):
        self.aggregate_asset_data(property_id)
        recommendations = []
        for asset_data in self.asset_data:
            if asset_data["utilization_rate"] < 50:
                recommendations.append(f"Consider reassigning or retiring {asset_data['asset_type']}")
        self.optimization_recommendations = recommendations
        self.save()

