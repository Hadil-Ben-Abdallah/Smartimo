from django.db import models
from core.models import Notification
from lease_rental_management.models import Tenant, PropertyManager
from tenant_screening_and_background_checks.models import ScreeningReport

class TenantScreeningServiceIntegration(models.Model):
    id = models.AutoField(primary_key=True)
    service_provider = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)

    def initiate_screening_request(self, tenant_info):
        screening_request_id = self.service_provider.initiate_screening(tenant_info, self.api_key)
        return screening_request_id

    def retrieve_screening_report(self, screening_request_id):
        report = self.service_provider.get_report(screening_request_id, self.api_key)
        return report

    def display_screening_results(self):
        results = self.retrieve_screening_report(self.integration_id)
        return results

    def validate_service_credentials(self):
        validation_status = self.service_provider.validate_credentials(self.api_key)
        return validation_status


class ScreeningWorkflowAutomation(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    trigger_conditions = models.JSONField(blank=True, null=True)
    screening_criteria = models.JSONField(blank=True, null=True)
    notification_preferences = models.JSONField(blank=True, null=True)

    def define_trigger_conditions(self, conditions):
        self.trigger_conditions = conditions
        self.save()

    def set_screening_criteria(self, criteria):
        self.screening_criteria = criteria
        self.save()

    def configure_notifications(self, preferences):
        self.notification_preferences = preferences
        self.save()

    def execute_workflow(self):
        if self.check_conditions_met():
            screening_request_id = TenantScreeningServiceIntegration.objects.get(
                service_provider="YourServiceProvider"
            ).initiate_screening_request(self.get_tenant_info())
            self.send_notifications(screening_request_id)


class ScreeningAuthorizationForm(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("signed", "Signed"), ("submitted", "Submitted")], default='pending')

    def generate_form(self, tenant):
        self.tenant = tenant
        self.content = "Please sign to authorize the screening."
        self.status = "pending"
        self.save()

    def send_form_to_tenant(self):
        self.status = "submitted"
        self.save()

    def receive_signed_form(self):
        self.status = "signed"
        self.save()

    def store_form(self):
        self.status = 'submitted'
        self.save()


class ScreeningAlertNotification(Notification):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    screening_report = models.ForeignKey(ScreeningReport, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=255, blank=True, null=True)

    def generate_alert(self, alert_type):
        if self.screening_report.credit_score < 600:
            self.alert_type = 'Negative Credit History'
        elif self.screening_report.criminal_summary:
            self.alert_type = 'Criminal Record'
        self.save()

    def log_alert_activity(self):
        TenantScreeningAuditTrail.objects.create(
            tenant=self.tenant, activity_type="Alert Generated", details=self.alert_type)

    def review_alert(self):
        return f"Alert reviewed: {self.alert_type}"


class TenantScreeningAuditTrail(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def log_activity(self, activity_type, details):
        self.activity_type = activity_type
        self.details = details
        self.save()

    def retrieve_audit_trail(self, tenant):
        return TenantScreeningAuditTrail.objects.filter(tenant=tenant)

    def archive_audit_records(self):
        pass

