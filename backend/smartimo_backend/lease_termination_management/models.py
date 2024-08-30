from django.db import models
from core.models import Property
from lease_rental_management.models import Tenant, PropertyManager, LeaseAgreement
from remote_property_monitoring.models import Inspector

class LeaseTermination(models.Model):
    id = models.AutoField(primary_key=True)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    notice_date = models.DateField(auto_now_add=True, blank=True, null=True)
    move_out_date = models.DateField(blank=True, null=True)
    forwarding_address = models.CharField(max_length=255, blank=True, null=True)
    termination_reason = models.TextField(blank=True, null=True)
    termination_status = models.CharField(max_length=50, choices=[
        ('initiated', 'Initiated'),
        ('pending_inspection', 'Pending Inspection'),
        ('completed', 'Completed')
    ], default='initiated')

    def submit_termination_notice(self, tenant_id, lease_id, property_manager_id, move_out_date, forwarding_address, termination_reason):
        self.tenant = tenant_id
        self.lease = lease_id
        self.property_manager = property_manager_id
        self.move_out_date = move_out_date
        self.forwarding_address = forwarding_address
        self.termination_reason = termination_reason
        self.termination_status = 'initiated'
        self.save()
        return self

    def update_status(self, status):
        self.termination_status = status
        self.save()
        return self

    def get_termination_details(self, termination_id):
        return LeaseTermination.objects.get(id=termination_id)

class MoveOutGuidance(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guidance_content = models.TextField(blank=True, null=True)
    checklist = models.JSONField(blank=True, null=True)
    faqs = models.JSONField(blank=True, null=True)

    def create_guidance(self, property_manager_id, property_id, guidance_content, checklist, faqs):
        self.property_manager = property_manager_id
        self.property = property_id
        self.guidance_content = guidance_content
        self.checklist = checklist
        self.faqs = faqs
        self.save()
        return self

    def view_guidance(self, tenant_id):
        lease = LeaseAgreement.objects.get(tenant=tenant_id)
        return MoveOutGuidance.objects.get(propert=lease.property.property_id)

    def customize_guidance(self, property_manager_id, guidance_id, updates):
        guidance = MoveOutGuidance.objects.get(id=guidance_id, property_manager=property_manager_id)
        for key, value in updates.items():
            setattr(guidance, key, value)
        guidance.save()
        return guidance

class PropertyInspection(models.Model):
    id = models.AutoField(primary_key=True)
    termination = models.ForeignKey(LeaseTermination, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    scheduled_date = models.DateField(blank=True, null=True)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE)
    inspection_checklist = models.JSONField(blank=True, null=True)
    inspection_results = models.JSONField(blank=True, null=True)
    photos = models.JSONField(blank=True, null=True)

    def schedule_inspection(self, termination_id, scheduled_date):
        self.termination = termination_id
        self.scheduled_date = scheduled_date
        self.save()
        return self

    def conduct_inspection(self, inspection_id, inspection_results, photos):
        inspection = PropertyInspection.objects.get(id=inspection_id)
        inspection.inspection_results = inspection_results
        inspection.photos = photos
        inspection.save()
        return inspection

    def view_inspection_report(self, inspection_id):
        return PropertyInspection.objects.get(id=inspection_id)

class SecurityDepositRefund(models.Model):
    id = models.AutoField(primary_key=True)
    termination = models.ForeignKey(LeaseTermination, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deductions = models.JSONField(blank=True, null=True)
    refund_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('completed', 'Completed')
    ], default='pending')
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check')
    ])

    def calculate_refund(self, termination_id):
        termination = LeaseTermination.objects.get(id=termination_id)
        deductions = {'damages': 100, 'cleaning': 50}
        self.refund_amount = termination.lease.security_deposit - sum(deductions.values())
        self.deductions = deductions
        self.termination = termination
        self.refund_status = 'pending'
        self.save()
        return self

    def generate_refund_statement(self, termination_id):
        refund = SecurityDepositRefund.objects.get(termination=termination_id)
        statement = {
            'refund_amount': refund.refund_amount,
            'deductions': refund.deductions,
            'refund_status': refund.refund_status
        }
        return statement

    def process_refund(self, refund_id, payment_method):
        refund = SecurityDepositRefund.objects.get(id=refund_id)
        refund.payment_method = payment_method
        refund.payment_date = models.DateField(auto_now_add=True)
        refund.refund_status = 'processed'
        refund.save()
        return refund

class LeaseTerminationConfirmation(models.Model):
    id = models.AutoField(primary_key=True)
    termination = models.ForeignKey(LeaseTermination, on_delete=models.CASCADE)
    confirmation_date = models.DateField(auto_now_add=True, blank=True, null=True)
    confirmation_details = models.JSONField(blank=True, null=True)

    def send_confirmation(self, termination_id):
        confirmation_details = {
            'termination': termination_id,
            'confirmation_date': self.confirmation_date,
            'details': 'Lease termination confirmed, refund processed.'
        }
        self.termination = LeaseTermination.objects.get(id=termination_id)
        self.confirmation_details = confirmation_details
        self.save()
        return self

    def view_confirmation(self, tenant_id):
        lease_termination = LeaseTermination.objects.get(tenant=tenant_id)
        return LeaseTerminationConfirmation.objects.get(termination=lease_termination.id)

