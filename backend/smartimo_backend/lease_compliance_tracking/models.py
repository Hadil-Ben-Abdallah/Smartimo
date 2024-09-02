from django.db import models
from django.utils import timezone
from lease_rental_management.models import LeaseAgreement, Tenant
from core.models import Reminder, TimeStampedModel

class LeaseReminder(Reminder):
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, choices=[('lease_renewal', 'Lease Renewal'), ('rent_escalation', 'Rent Escalation'), ('payment_due', 'Payment Due')], default='lease_renewal')
    custom_parameters = models.JSONField(blank=True, null=True)

    def customize_reminder_settings(self, reminder_id, settings):
        reminder = LeaseReminder.objects.get(id=reminder_id)
        reminder.custom_parameters = settings
        reminder.save()

class RentalPaymentHistory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    payment_date = models.DateField(blank=True, null=True)
    amount_paid = models.FloatField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('pending', 'Pending'), ('overdue', 'Overdue')], default='pending')
    payment_method = models.CharField(max_length=50, choices=[('bank_transfer', 'Bank Transfer'), ('credit_card', 'Credit Card'), ('cash', 'Cash')], default='credit_card')

    def log_payment(self, tenant_id, payment_details):
        RentalPaymentHistory.objects.create(
            lease=payment_details['lease_id'],
            tenant=tenant_id,
            payment_date=payment_details['payment_date'],
            amount_paid=payment_details['amount_paid'],
            payment_status=payment_details['payment_status'],
            payment_method=payment_details['payment_method']
        )

    def get_payment_history(self, tenant_id):
        return RentalPaymentHistory.objects.filter(tenant=tenant_id).values()

    def generate_payment_report(self, lease_id):
        payments = RentalPaymentHistory.objects.filter(lease=lease_id)
        report = {
            'total_payments': payments.count(),
            'total_amount': payments.aggregate(models.Sum('amount_paid'))['amount_paid__sum'],
            'details': list(payments.values())
        }
        return report

    def track_overdue_payments(self, tenant_id):
        overdue_payments = RentalPaymentHistory.objects.filter(
            tenant=tenant_id,
            payment_status='overdue'
        )
        return list(overdue_payments.values())

class MaintenanceCompliance(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    maintenance_task = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(null=True, blank=True)
    compliance_status = models.CharField(max_length=50, choices=[('compliant', 'Compliant'), ('non_compliant', 'Non-Compliant'), ('overdue', 'Overdue')], default='compliant')

    def log_maintenance_task(self, lease_id, task_details):
        MaintenanceCompliance.objects.create(
            lease=lease_id,
            tenant=task_details['tenant_id'],
            maintenance_task=task_details['maintenance_task'],
            due_date=task_details['due_date'],
            compliance_status='Overdue' if task_details['due_date'] < timezone.now().date() else 'Compliant'
        )

    def track_maintenance_compliance(self, lease_id):
        tasks = MaintenanceCompliance.objects.filter(lease=lease_id)
        return {
            'total_tasks': tasks.count(),
            'compliant_tasks': tasks.filter(compliance_status='Compliant').count(),
            'non_compliant_tasks': tasks.filter(compliance_status='Non-Compliant').count(),
            'overdue_tasks': tasks.filter(compliance_status='Overdue').count(),
            'details': list(tasks.values())
        }

    def generate_compliance_report(self, lease_id):
        compliance_data = self.track_maintenance_compliance(lease_id)
        report = {
            'total_tasks': compliance_data['total_tasks'],
            'compliant_tasks': compliance_data['compliant_tasks'],
            'non_compliant_tasks': compliance_data['non_compliant_tasks'],
            'overdue_tasks': compliance_data['overdue_tasks'],
            'details': compliance_data['details']
        }
        return report

    def address_non_compliance(self, tenant_id):
        non_compliant_tasks = MaintenanceCompliance.objects.filter(
            tenant_id=tenant_id,
            compliance_status='Non-Compliant'
        )
        return list(non_compliant_tasks.values())

class LegalCompliance(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    regulation = models.CharField(max_length=255, blank=True, null=True)
    compliance_status = models.CharField(max_length=50, choices=[('compliant', 'Compliant'), ('non_compliant', 'Non-Compliant')], default='compliant')
    discrepancies = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    def perform_compliance_check(self, lease_id):
        lease = LeaseAgreement.objects.get(id=lease_id)
        self.compliance_status = 'compliant'
        self.discrepancies = ''
        self.recommendations = ''
        self.save()

    def flag_discrepancies(self, lease_id):
        self.perform_compliance_check(lease_id)
        if self.compliance_status == 'non_compliant':
            self.discrepancies = 'Example discrepancy found'
            self.save()

    def generate_compliance_report(self, lease_id):
        self.perform_compliance_check(lease_id)
        report = {
            'lease': lease_id,
            'compliance_status': self.compliance_status,
            'discrepancies': self.discrepancies,
            'recommendations': self.recommendations
        }
        return report

    def recommend_amendments(self, lease_id):
        self.perform_compliance_check(lease_id)
        if self.compliance_status == 'non_compliant':
            recommendations = 'Recommended amendments to meet compliance'
            self.recommendations = recommendations
            self.save()
            return recommendations
        return 'Lease is compliant'

