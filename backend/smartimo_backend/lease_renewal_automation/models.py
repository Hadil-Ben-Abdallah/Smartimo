from django.db import models
from core.models import Reminder, Document, Communication, Notification
from lease_rental_management.models import Tenant, PropertyManager, LeaseAgreement

class LeaseRenewalReminder(Reminder):
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('sent', 'Sent'), ('opened', 'Opened'), ('responded', 'Responded'), ('expired', 'Expired')], default='pending')

    def customize_reminder(self, frequency, delivery_channel):
        self.reminder_frequency = frequency
        self.delivery_channel = delivery_channel
        self.save()

    def track_status(self):
        if self.status == 'opened':
            return 'Reminder opened by recipient'
        elif self.status == 'responded':
            return 'Recipient responded to the reminder'
        return 'Reminder not yet opened'

    def schedule_reminder(self, lead_time):
        lease_expiration_date = self.lease.end_date
        reminder_date = lease_expiration_date - lead_time
        self.reminder_date = reminder_date
        self.save()


class LeaseRenewalDocument(Document):
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    document_template = models.TextField(blank=True, null=True)
    custom_terms = models.TextField(blank=True, null=True)
    renewal_options = models.TextField(blank=True, null=True)
    attached_addendums = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('drafted', 'Drafted'), ('sent', 'Sent'), ('signed', 'Signed')], default='drafted')

    def generate_document(self):
        self.status = 'drafted'
        self.save()

    def customize_document(self, custom_terms, renewal_options, addendums):
        self.custom_terms = custom_terms
        self.renewal_options = renewal_options
        self.attached_addendums = addendums
        self.save()

    def integrate_with_esignature(self):
        self.status = 'sent'
        self.save()


class LeaseRenewalCommunication(Communication):
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('sent', 'Sent'), ('received', 'Received'), ('responded', 'Responded')], default='sent')
    version_control = models.CharField(max_length=50, blank=True, null=True)

    def send_renewal_offer(self, offer_details):
        self.status = 'sent'
        self.save()

    def track_communication(self):
        history = {
            'lease': self.lease.id,
            'status': self.status,
            'version': self.version_control,
        }
        return history

    def manage_negotiation(self, tenant_response):
        self.tenant_response = tenant_response
        self.status = 'responded'
        self.save()


class TenantNotification(Notification):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)

    def track_response(self):
        response_status = 'Response tracked successfully'
        return response_status

    def display_notifications(self):
        notifications = {
            'tenant': self.tenant.user_id,
            'lease': self.lease.id,
        }
        return notifications


class LeaseRenewalProgress(models.Model):
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    renewal_status = models.CharField(max_length=50, choices=[('initiated', 'Initiated'), ('in_negotiation', 'In Negotiation'), ('completed', 'Completed')])
    response_rate = models.FloatField(blank=True, null=True)
    renewal_rate = models.FloatField(blank=True, null=True)
    pending_tasks = models.TextField(blank=True, null=True)

    def track_progress(self):
        progress = {
            'renewal_status': self.renewal_status,
            'response_rate': self.response_rate,
            'renewal_rate': self.renewal_rate,
            'pending_tasks': self.pending_tasks,
        }
        return progress

    def generate_status_reports(self):
        report = {
            'lease_id': self.lease.id,
            'property_manager_id': self.property_manager.user_id,
            'renewal_status': self.renewal_status,
        }
        return report

    def send_alerts(self, alert_message):
        alert_status = f'Alert sent: {alert_message}'
        return alert_status

    def coordinate_renewal_efforts(self):
        coordination_status = 'Coordination successful'
        return coordination_status

