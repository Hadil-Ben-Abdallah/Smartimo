from django.db import models
from datetime import datetime, timedelta
from core.models import Notification, Report
from lease_rental_management.models import Tenant, LeaseAgreement, PropertyManager
from property_listing.models import PropertyOwner
from tenant_portal_maintenance_tracking.models import MaintenanceTask


class LeaseNotification(Notification):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100, blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True, null=True)

    def customize_notification_settings(self, settings):
        self.preferences.update(settings)
        self.save()

    def schedule_notification(self):
        expiration_date = self.lease.end_date
        notification_date = expiration_date - timedelta(days=self.preferences.get('days_before', 30))
        if datetime.now().date() >= notification_date:
            self.send_notification()

    def send_notification(self):
        message = f"Notification Type: {self.notification_type}, Lease ID: {self.lease.id}."
        print(f"Sending notification: {message}")


class RentalPaymentTracker(models.Model):
    id = models.AutoField(primary_key=True)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('overdue', 'Overdue'), ('pending', 'Pending')], default='pending')
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)

    def track_payment(self, payment_date, payment_amount):
        self.payment_date = payment_date
        self.payment_amount = payment_amount
        self.outstanding_balance -= payment_amount
        self.payment_status = 'paid' if self.outstanding_balance <= 0 else 'overdue'
        self.save()

    def view_payment_history(self):
        return {
            "lease": self.lease.id,
            "tenant": self.tenant.user_id,
            "payment_date": self.payment_date,
            "payment_amount": self.payment_amount,
            "outstanding_balance": self.outstanding_balance,
            "payment_status": self.payment_status
        }

    def send_overdue_reminder(self):
        if self.payment_status == 'overdue':
            reminder_message = f"Dear {self.tenant.username}, your payment is overdue for Lease ID: {self.lease.id}."
            print(f"Sending reminder: {reminder_message}")

    def process_online_payment(self, amount):
        self.track_payment(payment_date=datetime.now().date(), payment_amount=amount)


class MaintenanceComplianceMonitor(models.Model):
    id = models.AutoField(primary_key=True)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    maintenance_task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    task_status = models.CharField(max_length=50, choices=[('scheduled', 'Scheduled'), ('assigned', 'Assigned'), ('completed', 'Completed')], default='scheduled')
    scheduled_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(null=True, blank=True)

    def schedule_task(self, task, date):
        self.maintenance_task = task
        self.scheduled_date = date
        self.task_status = 'scheduled'
        self.save()

    def assign_task(self, assignee):
        self.assigned_to = assignee
        self.task_status = 'assigned'
        self.save()

    def track_task_completion(self, completion_date):
        self.completion_date = completion_date
        self.task_status = 'completed'
        self.save()

    def generate_compliance_report(self):
        report = {
            "lease_id": self.lease.id,
            "maintenance_task": self.maintenance_task.id,
            "assigned_to": self.assigned_to,
            "task_status": self.task_status,
            "scheduled_date": self.scheduled_date,
            "completion_date": self.completion_date
        }
        return report


class LeaseInfoPortal(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    lease_terms = models.TextField(blank=True, null=True)
    payment_schedule = models.JSONField(default=dict, blank=True, null=True)
    maintenance_responsibilities = models.TextField(blank=True, null=True)
    maintenance_requests = models.JSONField(default=list, blank=True, null=True)

    def view_lease_details(self):
        return {
            "lease_terms": self.lease_terms,
            "payment_schedule": self.payment_schedule,
            "maintenance_responsibilities": self.maintenance_responsibilities
        }

    def submit_maintenance_request(self, request):
        self.maintenance_requests.append(request)
        self.save()

    def view_maintenance_schedule(self):
        return self.maintenance_requests

    def communicate_with_manager(self, message):
        print(f"Message from Tenant {self.tenant.username} to Manager: {message}")


class LeaseComplianceReport(Report):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    rental_income = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    compliance_status = models.CharField(max_length=50, blank=True, null=True)
    maintenance_summary = models.TextField(blank=True, null=True)
    tenant_communications = models.JSONField(default=list, blank=True, null=True)

    def generate_report(self):
        report = {
            "lease": self.lease.id,
            "rental_income": self.rental_income,
            "compliance_status": self.compliance_status,
            "maintenance_summary": self.maintenance_summary,
            "tenant_communications": self.tenant_communications
        }
        return report

    def view_compliance_trends(self):
        trends = {"compliance_status": self.compliance_status, "rental_income": self.rental_income}
        return trends

    def analyze_rental_income(self):
        projections = self.rental_income * 12
        return projections

    def recommend_improvements(self):
        recommendations = "Improve payment reminders and automate maintenance scheduling."
        return recommendations

