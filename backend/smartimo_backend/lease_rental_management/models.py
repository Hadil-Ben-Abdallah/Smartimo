from django.db import models
from core.models import Property, User, Communication
from django.utils import timezone

class LeaseAgreement(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lease_agreements')
    terms = models.JSONField(default=dict)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    signed_document = models.URLField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def create_lease_agreement(self):
        self.save()

    def update_lease_agreement(self, terms, rent_amount, security_deposit, start_date, end_date):
        self.terms = terms
        self.rent_amount = rent_amount
        self.security_deposit = security_deposit
        self.start_date = start_date
        self.end_date = end_date
        self.updated_at = timezone.now()
        self.save()

    def sign_lease_agreement(self, signed_document_url):
        self.signed_document = signed_document_url
        self.save()

    def get_lease_agreement(self):
        return {
            "id": self.id,
            "property": self.property.address,
            "tenant": self.tenant.username,
            "terms": self.terms,
            "rent_amount": self.rent_amount,
            "security_deposit": self.security_deposit,
            "signed_document": self.signed_document,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

class Tenant(User):
    lease_agreements = models.ManyToManyField(LeaseAgreement, related_name='tenants')
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
            type='inquiry',
            message=inquiry['message']
        )
        return communication

class PropertyManager(User):
    properties = models.ManyToManyField(Property, related_name='managers')
    lease_agreements = models.ManyToManyField(LeaseAgreement, related_name='property_managers')

    def create_lease_agreement(self, property, tenant, terms, rent_amount, security_deposit, start_date, end_date):
        lease_agreement = LeaseAgreement.objects.create(
            property=property,
            tenant=tenant,
            terms=terms,
            rent_amount=rent_amount,
            security_deposit=security_deposit,
            start_date=start_date,
            end_date=end_date
        )
        self.lease_agreements.add(lease_agreement)

    def update_lease_agreement(self, terms, rent_amount, security_deposit, start_date, end_date):
        LeaseAgreement.terms = terms
        LeaseAgreement.rent_amount = rent_amount
        LeaseAgreement.security_deposit = security_deposit
        LeaseAgreement.start_date = start_date
        LeaseAgreement.end_date = end_date
        LeaseAgreement.updated_at = timezone.now()
        LeaseAgreement.save()

    def track_rental_payments(self):
        return RentalPayment.objects.filter(lease_agreement__in=self.lease_agreements.all())

    def generate_rental_reports(self):
        payments = self.track_rental_payments()
        report = {}
        for payment in payments:
            if payment.lease_agreement.property.property_id not in report:
                report[payment.lease_agreement.property.property_id] = 0
            report[payment.lease_agreement.property.property_id] += payment.amount
        return report

    def respond_to_inquiry(self, inquiry_id, response):
        communication = LeaseRentalCommunication.objects.get(id=inquiry_id)
        communication.response = response
        communication.save()
        return communication

class RentalPayment(models.Model):
    id = models.AutoField(primary_key=True)
    lease_agreement = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='pending')

    def make_payment(self, amount, payment_method):
        self.amount = amount
        self.payment_method = payment_method
        self.payment_date = timezone.now()
        self.status = 'completed'
        self.save()

    def send_payment_reminder(self):
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
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    response = models.TextField(blank=True, null=True)

    def get_messages(self):
        return LeaseRentalCommunication.objects.filter(tenant=self.tenant, manager=self.manager)

    def log_communication(self, message):
        LeaseRentalCommunication.objects.create(tenant=self.tenant, manager=self.manager, type=self.type, message=message)

