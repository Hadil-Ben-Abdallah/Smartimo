from django.db import models
from core.models import Reminder, Notification, Report
from lease_rental_management.models import Tenant, PropertyManager
from maintenance_and_service_requests.models import MaintenanceTechnician
from property_listing.models import PropertyOwner
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail

class RentReminder(Reminder):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def schedule_reminder(self, days_before_due=3):
        rent_due_date = self.tenant.lease_agreements.end_date
        self.reminder_date = rent_due_date - timedelta(days=days_before_due)
        self.save()

    def customize_message_content(self, custom_message):
        self.reminder_message = custom_message
        self.save()

    def track_reminder_status(self):
        return self.status

    def view_tenant_response_rate(self):
        response_rate = self.tenant.view_payment_history.filter(date__gte=self.scheduled_time).count()
        return response_rate

    def send_reminder(self):
        if timezone.now() >= self.reminder_date and not self.status == 'sent':
            send_mail(
                'Rent Reminder',
                self.message_content,
                'from@example.com',
                [self.tenant.email],
                fail_silently=False,
            )
            self.status = 'sent'
            self.save()

class LeaseRenewalNotification(Notification):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease_end_date = models.DateField(blank=True, null=True)

    def identify_eligible_tenants(self):
        expiring_soon = Tenant.objects.filter(leaseagreement__end_date__lte=timezone.now() + timedelta(days=30))
        return expiring_soon

    def configure_workflow_triggers(self, notification_days_before=30):
        self.lease_end_date = self.tenant.lease_agreements.end_date
        self.created_at = self.lease_end_date - timedelta(days=notification_days_before)
        self.save()

    def track_renewal_status(self):
        renewal_status = self.tenant.lease_agreements.filter(end_date__gt=timezone.now()).exists()
        return "Renewed" if renewal_status else "Pending"
    
    def send_renewal_notification(self):
        if timezone.now() >= self.created_at:
            send_mail(
                'Lease Renewal Notice',
                self.notification_content,
                'from@example.com',
                [self.tenant.email],
                fail_silently=False,
            )

class AutomatedFinancialReport(Report):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    report_date = models.DateField(auto_now_add=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('generated', 'Generated'), ('sent', 'Sent')],default="generated")

    def generate_report(self):
        self.income = self.property_manager.calculate_total_income()
        self.expenses = self.property_manager.calculate_total_expenses()
        self.net_income = self.income - self.expenses
        self.save()

    def schedule_report_generation(self):
        next_report_date = timezone.now().replace(day=1) + timedelta(days=32)
        next_report_date = next_report_date.replace(day=1)
        self.report_date = next_report_date
        self.save()

    def customize_report_layout(self, custom_layout):
        self.status = f"Customized - {custom_layout}"
        self.save()

    def view_report_status(self):
        return self.status
    
    def distribute_report(self):
        send_mail(
            'Monthly Financial Report',
            f"Your report for {self.report_date} is ready.\nNet Income: {self.net_income}",
            'from@example.com',
            [self.owner.email],
            fail_silently=False,
        )
        self.status = "Sent"
        self.save()

class InspectionReminder(Reminder):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    maintenance_staff = models.ManyToManyField(MaintenanceTechnician, blank=True, null=True)

    def schedule_inspection(self, frequency_days=180):
        self.reminder_date = timezone.now() + timedelta(days=frequency_days)
        self.save()

    def customize_inspection_template(self, custom_message, checklist):
        self.message_content = f"{custom_message}\n\nChecklist:\n{checklist}"
        self.save()

    def track_inspection_status(self):
        return self.status
    
    def send_inspection_reminder(self):
        if timezone.now() >= self.reminder_date and not self.status == 'sent':
            for staff in self.maintenance_staff.all():
                send_mail(
                    'Property Inspection Reminder',
                    self.message_content,
                    'from@example.com',
                    [self.tenant.email, staff.email],
                    fail_silently=False,
                )
            self.sent_status = True
            self.save()

