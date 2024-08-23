from django.db import models
from django.utils import timezone
from vendor_management.models import Vendor
from core.models import Property


class VendorMarketplace(models.Model):
    id = models.AutoField(primary_key=True)
    service_categories = models.JSONField(blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True, null=True)

    def search_vendors(self, service_type=None, location=None, rating=None):
        vendors = self.vendors.all()
        if service_type:
            vendors = vendors.filter(service_categories__contains=[service_type])
        if location:
            vendors = vendors.filter(service_areas__icontains=location)
        if rating:
            vendors = vendors.filter(customer_reviews__contains=[rating])
        return vendors

    def browse_vendors(self, category=None, location=None):
        vendors = self.vendors.all()
        if category:
            vendors = vendors.filter(service_categories__contains=[category])
        if location:
            vendors = vendors.filter(service_areas__icontains=location)
        return vendors

    def view_vendor_profile(self, vendor_id):
        return Vendor.objects.get(pk=vendor_id)


class QuoteResponse(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    quote_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)

    def submit_quote(self, vendor_id, quote_amount, service_description):
        self.vendor_id = Vendor.objects.get(pk=vendor_id)
        self.quote_amount = quote_amount
        self.service_description = service_description
        self.response_date = timezone.now()
        self.save()

    def update_quote(self, quote_amount, service_description):
        self.quote_amount = quote_amount
        self.service_description = service_description
        self.save()


class QuoteRequest(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=255, choices=[('maintenance', 'Maintenance'), ('cleaning', 'Cleaning')], default='maintenance')
    request_details = models.TextField(blank=True, null=True)
    vendor_responses = models.ManyToManyField(QuoteResponse, blank=True, null=True)

    def submit_request(self, property_id, service_type, request_details):
        self.property.property_id = property_id
        self.service_type = service_type
        self.request_details = request_details
        self.save()

    def review_responses(self):
        return self.vendor_responses.all()

    def select_vendor(self, response_id):
        response = QuoteResponse.objects.get(pk=response_id)
        return response.vendor.id


class VendorMarketplacePerformance(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    performance_metrics = models.JSONField(blank=True, null=True)
    feedback = models.JSONField(blank=True, null=True)

    def track_performance(self, vendor_id, metrics):
        self.vendor.id = Vendor.objects.get(pk=vendor_id)
        self.performance_metrics = metrics
        self.save()

    def collect_feedback(self, feedback):
        self.feedback.extend(feedback)
        self.save()

    def generate_report(self):
        report = {
            'vendor_id': self.vendor.id,
            'performance_metrics': self.performance_metrics,
            'feedback': self.feedback,
        }
        return report


class ContractManagement(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    contract_terms = models.TextField(blank=True, null=True)
    contract_document = models.FileField(upload_to='contracts/, blank=True, null=True')
    payment_schedule = models.JSONField(blank=True, null=True)

    def create_contract(self, vendor_id, contract_terms, document, payment_schedule):
        self.vendor.id = Vendor.objects.get(pk=vendor_id)
        self.contract_terms = contract_terms
        self.contract_document = document
        self.payment_schedule = payment_schedule
        self.save()

    def sign_contract(self):
        return f"Contract {self.id} signed."

    def manage_payments(self, payments):
        for payment in payments:
            PaymentTransaction.objects.create(
                id=self,
                amount=payment['amount'],
                transaction_date=timezone.now(),
                payment_status=payment['status']
            )


class PaymentTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(ContractManagement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)

    def process_payment(self, amount):
        self.amount = amount
        self.transaction_date = timezone.now()
        self.payment_status = 'completed'
        self.save()

    def track_transaction(self):
        return {
            'transaction_id': self.id,
            'amount': self.amount,
            'status': self.payment_status,
            'date': self.transaction_date
        }

    def generate_invoice(self):
        return {
            'transaction_id': self.id,
            'amount': self.amount,
            'status': self.payment_status
        }
