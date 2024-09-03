from django.db import models
from core.models import Notification, Report, TimeStampedModel
from lease_rental_management.models import Tenant
from property_listing.models import PropertyOwner
from django.utils import timezone
import stripe
import paypalrestsdk
from django.core.mail import send_mail
from django.conf import settings

class PaymentGateway(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    enabled = models.BooleanField(default=True, blank=True, null=True)

    def process_payment(self, payment_details):
        if not self.enabled:
            raise Exception("Payment gateway is not enabled.")
        
        if self.name == "Stripe":
            stripe.api_key = self.api_key
            try:
                charge = stripe.Charge.create(
                    amount=int(payment_details['amount'] * 100),  # Amount in cents
                    currency="usd",
                    source=payment_details['source'],
                    description=payment_details['description'],
                )
                return charge
            except stripe.error.StripeError as e:
                raise Exception(f"Stripe payment failed: {e.user_message}")
        
        elif self.name == "PayPal":
            paypalrestsdk.configure({
                "mode": "live",
                "client_id": self.api_key,
                "client_secret": payment_details['client_secret']
            })
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"},
                "transactions": [{
                    "amount": {
                        "total": str(payment_details['amount']),
                        "currency": "USD"},
                    "description": payment_details['description']}],
                "redirect_urls": {
                    "return_url": payment_details['return_url'],
                    "cancel_url": payment_details['cancel_url']}
            })

            if payment.create():
                return payment
            else:
                raise Exception(f"PayPal payment failed: {payment.error}")

        else:
            raise Exception("Unsupported payment gateway.")

    def validate_payment(self, payment_response):
        if self.name == "Stripe":
            if payment_response['status'] == "succeeded":
                return True
            else:
                raise Exception("Stripe payment validation failed.")
        
        elif self.name == "PayPal":
            if payment_response['state'] == "approved":
                return True
            else:
                raise Exception("PayPal payment validation failed.")
        
        else:
            raise Exception("Unsupported payment gateway.")


class RecurringPayment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    frequency = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('canceled', 'Canceled')],default='active')

    def setup_recurring_payment(self):
        self.status = "active"
        self.save()

    def modify_recurring_payment(self, new_amount=None, new_frequency=None, new_start_date=None):
        if new_amount:
            self.amount = new_amount
        if new_frequency:
            self.frequency = new_frequency
        if new_start_date:
            self.start_date = new_start_date
        self.save()

    def cancel_recurring_payment(self):
        self.status = 'canceled'
        self.save()

    def process_recurring_payment(self):
        if self.status != 'active':
            raise Exception("Recurring payment is not active.")
        payment_details = {
            'amount': self.amount,
            'description': f"Recurring rent payment for Tenant ID {self.tenant.user_id}"
        }
        payment_gateway = PaymentGateway.objects.filter(enabled=True).first()
        payment_response = payment_gateway.process_payment(payment_details)
        if payment_gateway.validate_payment(payment_response):
            RentPayment.objects.create(
                tenant=self.tenant,
                amount=self.amount,
                payment_date=timezone.now(),
                status='successful',
                gateway=payment_gateway
            )


class RentPayment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('successful', 'Successful'), ('failed', 'Failed')], default='successful')
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.CASCADE)

    def initiate_payment(self, payment_details):
        payment_gateway = PaymentGateway.objects.get(id=payment_details['gateway_id'])
        payment_response = payment_gateway.process_payment(payment_details)
        self.payment_date = timezone.now()
        if payment_gateway.validate_payment(payment_response):
            self.status = 'successful'
        else:
            self.status = 'failed'
        self.save()

    def confirm_payment(self):
        pass


class LateFee(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    rent_payment = models.ForeignKey(RentPayment, on_delete=models.CASCADE)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    applied_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def calculate_late_fee(self):
        days_overdue = (timezone.now().date() - self.rent_payment.payment_date.date()).days
        if days_overdue > 0:
            self.fee_amount = self.rent_payment.amount * 0.05
            return self.fee_amount
        return 0

    def apply_late_fee(self):
        self.calculate_late_fee()
        if self.fee_amount > 0:
            self.save()


class RentNotification(Notification):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255)

    def send_rent_due_notification(self):
        subject = "Rent Due Notification"
        body = (
            f"Dear {self.tenant.username},\n\n"
            "This is a reminder that your rent is due. Please make sure to submit your payment on time.\n\n"
            "Thank you,\nThe Smartimo Team"
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [self.tenant.email])
        return f"The rent due notification email to {self.tenant.username} has been sent successfully."

    def send_payment_received_notification(self):
        subject = "Payment Received"
        body = (
            f"Dear {self.tenant.username},\n\n"
            "We have received your payment. Thank you!\n\n"
            "Thank you,\nThe Smartimo Team"
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [self.tenant.email])
        return f"The payment received notification email to {self.tenant.username} has been sent successfully."

    def send_late_fee_notification(self):
        subject = "Late Fee Applied"
        body = (
            f"Dear {self.tenant.username},\n\n"
            "A late fee has been applied to your account due to a missed payment deadline. Please make your payment as soon as possible.\n\n"
            "Thank you,\nThe Smartimo Team"
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [self.tenant.email])
        return f"The late fee notification email to {self.tenant.username} has been sent successfully."


class RentCollectionReport(Report):
    landlord = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    report_data = models.JSONField(blank=True, null=True)

    def generate_report(self):
        self.report_data = {
            'total_collected': RentPayment.objects.aggregate(models.Sum('amount'))['amount__sum'],
            'on_time_payments': RentPayment.objects.filter(status='successful').count(),
            'late_fees_collected': LateFee.objects.aggregate(models.Sum('fee_amount'))['fee_amount__sum'],
        }
        self.save()

    def filter_report(self, criteria):
        filtered_data = {}
        if 'date_range' in criteria:
            start_date, end_date = criteria['date_range']
            filtered_data = {
                'filtered_collected': RentPayment.objects.filter(
                    payment_date__range=(start_date, end_date)
                ).aggregate(models.Sum('amount'))['amount__sum'],
            }
        return filtered_data

    def visualize_data(self):
        visualization_data = {
            'rent_collected': self.report_data['total_collected'],
            'on_time': self.report_data['on_time_payments'],
            'late_fees': self.report_data['late_fees_collected'],
        }
        return visualization_data
