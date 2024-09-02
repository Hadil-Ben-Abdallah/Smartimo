from django.db import models
from core.models import Property, TimeStampedModel
from lease_rental_management.models import Tenant

class AccessControlSystem(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    control_hardware = models.JSONField(blank=True, null=True)
    software_integration = models.JSONField(blank=True, null=True)
    access_policies = models.JSONField(blank=True, null=True)
    access_logs = models.JSONField(blank=True, null=True)

    def configure_access_policies(self, policies):
        self.access_policies = policies
        self.save()

    def issue_credentials(self, personnel):
        if 'authorized_personnel' not in self.access_policies:
            self.access_policies['authorized_personnel'] = []
        self.access_policies['authorized_personnel'].append(personnel)
        self.save()

    def monitor_access(self, activity_logs):
        self.access_logs = activity_logs
        self.save()

    def analyze_access_logs(self):
        suspicious_activity = [log for log in self.access_logs if log.get('status') == 'unauthorized']
        return suspicious_activity

class SurveillanceSystem(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    camera_details = models.JSONField(blank=True, null=True)
    recording_schedules = models.JSONField(blank=True, null=True)
    motion_detection_settings = models.JSONField(blank=True, null=True)
    video_storage = models.JSONField(blank=True, null=True)

    def configure_camera_settings(self, camera_details):
        self.camera_details = camera_details
        self.save()

    def monitor_surveillance(self):
        live_feeds = [camera['feed_url'] for camera in self.camera_details]
        return live_feeds

    def review_footage(self, time_range):
        footage = [video for video in self.video_storage if video['timestamp'] in time_range]
        return footage

    def export_footage(self, incident_id):
        incident_footage = [video for video in self.video_storage if video['incident_id'] == incident_id]
        return incident_footage

class AlarmSystem(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    sensor_details = models.JSONField(blank=True, null=True)
    alarm_triggers = models.JSONField(blank=True, null=True)
    notification_channels = models.JSONField(blank=True, null=True)
    alarm_events = models.JSONField(blank=True, null=True)

    def configure_alarm_triggers(self, sensor_details):
        self.sensor_details = sensor_details
        self.save()

    def monitor_alarm_events(self):
        active_alarms = [event for event in self.alarm_events if event['status'] == 'active']
        return active_alarms

    def respond_to_alarm(self, alarm_id):
        alarm_event = next(event for event in self.alarm_events if event['id'] == alarm_id)
        alarm_event['status'] = 'responded'
        self.save()

    def analyze_alarm_events(self):
        event_analysis = {'breaches': 0, 'false_alarms': 0}
        for event in self.alarm_events:
            if event['status'] == 'breach':
                event_analysis['breaches'] += 1
            elif event['status'] == 'false_alarm':
                event_analysis['false_alarms'] += 1
        return event_analysis

class TenantSecurityPortal(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    security_info = models.JSONField(blank=True, null=True)
    emergency_protocols = models.JSONField(blank=True, null=True)
    distress_alerts = models.JSONField(blank=True, null=True)

    def access_security_info(self):
        return self.security_info

    def initiate_distress_alert(self):
        alert = {"tenant": self.tenant.user_id, "status": "active"}
        self.distress_alerts.append(alert)
        self.save()
        return alert

    def report_security_concern(self, concern_details):
        concern = {"details": concern_details, "status": "reported"}
        if 'concerns' not in self.distress_alerts:
            self.distress_alerts['concerns'] = []
        self.distress_alerts['concerns'].append(concern)
        self.save()

    def receive_security_updates(self):
        updates = {"advisories": "Be cautious of...", "safety_tips": "Remember to..."}
        return updates

class SecurityAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    access_control_data = models.JSONField(blank=True, null=True)
    surveillance_data = models.JSONField(blank=True, null=True)
    alarm_data = models.JSONField(blank=True, null=True)
    incident_reports = models.JSONField(blank=True, null=True)
    analytics_tools = models.JSONField(blank=True, null=True)

    def aggregate_security_data(self):
        aggregated_data = {
            "access_control": self.access_control_data,
            "surveillance": self.surveillance_data,
            "alarm": self.alarm_data,
        }
        return aggregated_data

    def generate_incident_reports(self):
        reports = {
            "total_incidents": len(self.incident_reports),
            "detailed_reports": self.incident_reports,
        }
        return reports

    def conduct_anomaly_detection(self):
        anomalies = {"access_control": [], "surveillance": [], "alarm": []}
        for entry in self.access_control_data:
            if entry.get("anomaly"):
                anomalies["access_control"].append(entry)
        for entry in self.surveillance_data:
            if entry.get("anomaly"):
                anomalies["surveillance"].append(entry)
        for entry in self.alarm_data:
            if entry.get("anomaly"):
                anomalies["alarm"].append(entry)
        return anomalies

    def recommend_security_measures(self):
        recommendations = ["Increase camera coverage", "Update alarm triggers", "Revise access policies"]
        return recommendations

