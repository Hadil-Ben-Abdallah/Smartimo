from django.db import models
from core.models import Communication, TimeStampedModel
from lease_rental_management.models import PropertyManager, Tenant
from lease_renewal_automation.models import LeaseRenewalReminder


class RenewalTrackingDashboard(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    renewal_data = models.JSONField(blank=True, null=True)

    def display_renewal_status(self):
        renewal_status = {
            'pending_renewals': LeaseRenewalReminder.objects.filter(status='Pending').count(),
            'responded_renewals': LeaseRenewalReminder.objects.filter(status='Responded').count(),
            'expired_renewals': LeaseRenewalReminder.objects.filter(status='Expired').count(),
        }
        return renewal_status

    def generate_reports(self):
        reports = {
            'total_renewals': LeaseRenewalReminder.objects.count(),
            'pending_responses': LeaseRenewalReminder.objects.filter(status='Pending').count(),
            'successful_renewals': LeaseRenewalReminder.objects.filter(status='Responded').count(),
        }
        return reports

    def customize_alerts(self, alert_type, frequency):
        self.renewal_data['alert_type'] = alert_type
        self.renewal_data['frequency'] = frequency
        self.save()

    def export_data(self):
        return self.renewal_data

class FollowUpCommunication(Communication):
    reminder = models.ForeignKey(LeaseRenewalReminder, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    response_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Responded', 'Responded'), ('sent', 'Sent')], default='pending')

    def schedule_follow_up(self):
        follow_up = FollowUpCommunication(reminder=self.reminder, recipient=self.recipient.user_id, response_status='Pending')
        follow_up.save()

    def send_follow_up(self):
        self.response_status = 'Sent'
        self.save()

    def track_follow_up_status(self):
        return self.response_status

    def escalate_communication(self):
        if self.response_status == 'Pending':
            self.send_follow_up()

