from django.db import models
from core.models import Communication
from lease_rental_management.models import Tenant, PropertyManager

class EmergencyResponsePlan(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    protocols = models.TextField(blank=True, null=True)
    roles_and_responsibilities = models.TextField(blank=True, null=True)
    training_materials = models.TextField(blank=True, null=True)
    checklists = models.TextField(blank=True, null=True)

    def create_plan(self, protocols, roles_and_responsibilities, training_materials, checklists):
        self.protocols = protocols
        self.roles_and_responsibilities = roles_and_responsibilities
        self.training_materials = training_materials
        self.checklists = checklists
        self.save()

    def update_plan(self, protocols=None, roles_and_responsibilities=None, training_materials=None, checklists=None):
        if protocols:
            self.protocols = protocols
        if roles_and_responsibilities:
            self.roles_and_responsibilities = roles_and_responsibilities
        if training_materials:
            self.training_materials = training_materials
        if checklists:
            self.checklists = checklists
        self.save()

    def assign_roles(self, roles_and_responsibilities):
        self.roles_and_responsibilities = roles_and_responsibilities
        self.save()

    def schedule_training(self, training_materials):
        self.training_materials = training_materials
        self.save()

class EmergencyAlertCommunication(Communication):
    id = models.AutoField(primary_key=True)
    distribution_channels = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('sent', 'Sent'), ('acknowledged', 'Acknowledged')], default='pending')

    def create_alert(self, message_template, distribution_channels):
        self.message_template = message_template
        self.distribution_channels = distribution_channels
        self.status = 'pending'
        self.save()

    def send_alert(self):
        # Example:
        channels = self.distribution_channels.split(',')
        for channel in channels:
            # Simulate sending alert
            print(f"Sending alert via {channel}: {self.message_template}")
        self.status = 'sent'
        self.save()

    def update_alert_status(self, status):
        self.status = status
        self.save()

    def generate_alert_reports(self):
        report = f"Alert {self.id}: Status: {self.status}, Sent at: {self.date}"
        return report

class TenantEmergencyInformation(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    emergency_contacts = models.TextField(blank=True, null=True)
    safety_guidelines = models.TextField(blank=True, null=True)
    evacuation_routes = models.TextField(blank=True, null=True)
    interactive_features = models.TextField(blank=True, null=True)

    def update_information(self, emergency_contacts=None, safety_guidelines=None, evacuation_routes=None, interactive_features=None):
        if emergency_contacts:
            self.emergency_contacts = emergency_contacts
        if safety_guidelines:
            self.safety_guidelines = safety_guidelines
        if evacuation_routes:
            self.evacuation_routes = evacuation_routes
        if interactive_features:
            self.interactive_features = interactive_features
        self.save()

    def access_guidelines(self):
        return {
            "safety_guidelines": self.safety_guidelines,
            "evacuation_routes": self.evacuation_routes,
            "emergency_contacts": self.emergency_contacts,
            "interactive_features": self.interactive_features,
        }

    def request_assistance(self, request_message):
        # Handle assistance requests
        return f"Assistance requested: {request_message}"

class IncidentManagementDashboard(models.Model):
    id = models.AutoField(primary_key=True)
    incident_type = models.CharField(max_length=100, choices=[('fire', 'fire'), ('flood', 'Flood')], default='fire')
    status_updates = models.TextField(blank=True, null=True)
    response_metrics = models.TextField(blank=True, null=True)
    incident_log = models.TextField(blank=True, null=True)

    def log_incident(self, incident_type, status_updates, response_metrics, incident_log):
        self.incident_type = incident_type
        self.status_updates = status_updates
        self.response_metrics = response_metrics
        self.incident_log = incident_log
        self.save()

    def update_status(self, status_updates):
        self.status_updates = status_updates
        self.save()

    def track_response(self, response_metrics):
        self.response_metrics = response_metrics
        self.save()

    def generate_incident_reports(self):
        # Logic to generate a report for the incident
        report = f"Incident {self.id}: Type: {self.incident_type}, Status Updates: {self.status_updates}"
        return report

class PostIncidentReview(models.Model):
    id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(IncidentManagementDashboard, on_delete=models.CASCADE)
    findings = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    action_items = models.TextField(blank=True, null=True)

    def conduct_debriefing(self, findings, recommendations, action_items):
        self.findings = findings
        self.recommendations = recommendations
        self.action_items = action_items
        self.save()

    def document_findings(self, findings):
        self.findings = findings
        self.save()

    def create_action_plan(self, action_items):
        self.action_items = action_items
        self.save()

    def share_best_practices(self):
        # Share best practices across the platform
        return f"Best Practices: Findings: {self.findings}, Recommendations: {self.recommendations}"

