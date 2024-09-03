from django.db import models
from datetime import datetime
from core.models import Property, User, Report, TimeStampedModel

class Project(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateField(auto_now_add=True, blank=True, null=True)
    expected_return = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('planning', 'Planning'),
        ('under_construction', 'Under Construction'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ], default='planning')
    inspection_reports = models.JSONField(blank=True, null=True)

    def update_status(self, new_status):
        self.status = new_status
        self.save()
        return self.status

    def generate_budget_report(self):
        report = {
            'project_id': self.id,
            'budget': self.budget,
            'status': self.status,
        }
        return report

    def generate_timeline_report(self):
        report = {
            'project_id': self.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        return report

    def get_inspection_reports(self):
        return self.inspection_reports

class Inspector(User):
    certifications = models.JSONField(blank=True, null=True)
    assigned_projects = models.ManyToManyField(Project)

    def perform_inspection(self, project_id):
        project = Project.objects.get(id=project_id)
        report = self.generate_inspection_report(project_id)
        return report

    def update_certifications(self, new_certifications):
        self.certifications = new_certifications
        self.save()
        return self.certifications

    def get_assigned_projects(self):
        return self.assigned_projects.all()

    def generate_inspection_report(self, project_id):
        report = {
            'project_id': project_id,
            'inspection_date': datetime.now(),
        }
        return report


class SecurityDevice(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=255, choices=[('camera', 'Camera'), ('motion', 'Motion'), ('sensor', 'Sensor'), ('door/window_sensor', 'Door/Window Sensor'), ('smart_lock', 'Smart Lock')], default='camera')
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('configured', 'Configured')], default='inactive')
    last_maintenance_date = models.DateField(blank=True, null=True)

    def configure_device(self, device_id):
        device = SecurityDevice.objects.get(id=device_id)
        device.status = "configured"
        device.save()

    def get_live_feed(self, device_id):
        device = SecurityDevice.objects.get(id=device_id)
        return f"https://livefeed.example.com/{device_id}"

    def set_alert_thresholds(self, device_id, thresholds):
        device = SecurityDevice.objects.get(id=device_id)
        device.status = f"alert thresholds set: {thresholds}"
        device.save()

    def send_alert(self, device_id, alert_type):
        device = SecurityDevice.objects.get(id=device_id)
        print(f"Alert of type {alert_type} sent for device {device_id}")

class MaintenanceDevice(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=255, choices=[('HVAC_system', 'HVAC System'), ('water_heater', 'Water Heater'), ('electrical_panel', 'Electrical Panel')], default='HVAC_system')
    status = models.CharField(max_length=50, choices=[('operational', 'Operational'), ('malfunctioning', 'Malfunctioning')], default='operational')
    last_maintenance_date = models.DateField(blank=True, null=True)
    performance_metrics = models.JSONField(blank=True, null=True)

    def monitor_device(self, device_id):
        device = MaintenanceDevice.objects.get(id=device_id)
        return device.performance_metrics

    def schedule_maintenance(self, device_id, date):
        device = MaintenanceDevice.objects.get(id=device_id)
        device.last_maintenance_date = date
        device.save()

    def analyze_performance(self, device_id):
        device = MaintenanceDevice.objects.get(id=device_id)
        metrics = device.performance_metrics
        analysis = {"status": "good"}
        return analysis

    def send_maintenance_alert(self, device_id, alert_type):
        device = MaintenanceDevice.objects.get(id=device_id)
        print(f"Maintenance alert of type {alert_type} sent for device {device_id}")


class InspectionReport(Report):
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    findings = models.TextField(blank=True, null=True)
    compliance_status = models.CharField(max_length=50, blank=True, null=True)

    def conduct_virtual_inspection(self, inspector_id, property_id):
        inspector = Inspector.objects.get(inspector_id=inspector_id)
        return {"status": "completed", "inspector": inspector_id, "property": property_id}

    def annotate_findings(self, report_id, findings):
        report = InspectionReport.objects.get(id=report_id)
        report.findings = findings
        report.save()

    def update_compliance_status(self, report_id, status):
        report = InspectionReport.objects.get(id=report_id)
        report.compliance_status = status
        report.save()

    def generate_inspection_report(self, inspector_id, property_id):
        report = InspectionReport.objects.filter(inspector_id=inspector_id, property_id=property_id).first()
        if report:
            return {"report_id": report.id, "findings": report.findings, "compliance_status": report.compliance_status}
        else:
            return {"message": "No report found"}

class ConstructionMonitoring(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    camera_feeds = models.JSONField(blank=True, null=True)
    progress_photos = models.JSONField(blank=True, null=True)
    safety_compliance_checklists = models.JSONField(blank=True, null=True)

    def track_progress(self, monitoring_id):
        monitoring = ConstructionMonitoring.objects.get(id=monitoring_id)
        return {"progress_photos": monitoring.progress_photos, "camera_feeds": monitoring.camera_feeds}

    def upload_progress_photo(self, monitoring_id, photo):
        monitoring = ConstructionMonitoring.objects.get(id=monitoring_id)
        monitoring.progress_photos.append(photo)
        monitoring.save()

    def complete_safety_checklist(self, monitoring_id, checklist):
        monitoring = ConstructionMonitoring.objects.get(id=monitoring_id)
        monitoring.safety_compliance_checklists.append(checklist)
        monitoring.save()

    def generate_progress_report(self, project_id):
        monitoring = ConstructionMonitoring.objects.filter(project_id=project_id).first()
        if monitoring:
            return {"camera_feeds": monitoring.camera_feeds, "progress_photos": monitoring.progress_photos}
        else:
            return {"message": "No monitoring data found"}

