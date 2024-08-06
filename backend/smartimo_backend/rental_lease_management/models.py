from django.db import models
from django.utils import timezone
from core.models import User, Communication, Property


class LeaseRentalAgreement(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    # manager = models.ForeignKey(User, on_delete=models.CASCADE)
    terms = models.JSONField(default=dict)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    signed_document = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def create_lease_agreement(self, data):
        self.property = data['property']
        self.tenant = data['tenant']
        # self.manager = data['manager']
        self.terms = data.get('terms', {})
        self.signed_document = data.get('signed_document', '')
        self.save()

    def update_lease_agreement(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    def sign_lease_agreement(self, signed_document_url):
        self.signed_document = signed_document_url
        self.save()

    def get_lease_agreement(self):
        return {
            'property': self.property,
            'tenant': self.tenant,
            # 'manager': self.manager,
            'terms': self.terms,
            'signed_document': self.signed_document,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class LeaseRentalTenant(User):
    lease_agreements = models.ManyToManyField(LeaseRentalAgreement, related_name='tenants')
    payment_history = models.JSONField(default=list)

    def view_lease_agreement(self):
        return self.lease_agreements.all()

    def view_payment_history(self):
        return self.payment_history

    def download_receipt(self, payment_id):
        for payment in self.payment_history:
            if payment['id'] == payment_id:
                return payment['receipt']
        return None

    def submit_inquiry(self, inquiry):
        communication = LeaseRentalCommunication.objects.create(
            tenant=self,
            # manager=inquiry['manager'],
            type='inquiry',
            message=inquiry['message']
        )
        return communication

class PropertyManager(User):
    properties = models.ManyToManyField(Property, related_name='properties')
    lease_agreements = models.ManyToManyField(LeaseRentalAgreement, related_name='managers')

    def create_lease_agreement(self, data):
        lease_agreement = LeaseRentalAgreement.objects.create(
            property=data['property'],
            manager=self.user_id,
            terms=data.get('terms', {}),
            signed_document=data.get('signed_document', '')
        )
        return lease_agreement

    def update_lease_agreement(self, lease_agreement, data):
        for field, value in data.items():
            setattr(lease_agreement, field, value)
        lease_agreement.save()

    def track_rental_payments(self):
        payments = RentalPayment.objects.filter(lease_agreement__manager=self)
        return payments

    def generate_rental_reports(self):
        payments = self.track_rental_payments()
        report = {}
        for payment in payments:
            if payment.lease_agreement.property.id not in report:
                report[payment.lease_agreement.property.id] = 0
            report[payment.lease_agreement.property.id] += payment.amount
        return report

    def respond_to_inquiry(self, inquiry_id, response):
        communication = LeaseRentalCommunication.objects.get(id=inquiry_id)
        communication.response = response
        communication.save()
        return communication

class RentalPayment(models.Model):
    id = models.AutoField(primary_key=True)
    lease_agreement = models.ForeignKey(LeaseRentalAgreement, on_delete=models.CASCADE)
    tenant = models.ForeignKey(LeaseRentalTenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def make_payment(self, data):
        self.lease_agreement = data['lease_agreement']
        self.tenant = data['tenant']
        self.amount = data['amount']
        self.payment_date = data['payment_date']
        self.payment_method = data['payment_method']
        self.status = 'completed'
        self.save()

    def send_payment_reminder(self, tenant):
        pass

    def get_payment_status(self):
        return self.status

    def generate_receipt(self):
        receipt = {
            'id': self.id,
            'lease_agreement': self.lease_agreement.id,
            'tenant': self.tenant.user_id,
            'amount': self.amount,
            'payment_date': self.payment_date,
            'payment_method': self.payment_method,
            'status': self.status
        }
        return receipt

class LeaseRentalCommunication(Communication):
    tenant = models.ForeignKey(LeaseRentalTenant, on_delete=models.CASCADE)
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    response = models.TextField(blank=True, null=True)

    def get_messages(self):
        return LeaseRentalCommunication.objects.filter(tenant=self.tenant, manager=self.manager)

    def log_communication(self, message, response=None):
        self.message = message
        self.response = response
        self.save()
