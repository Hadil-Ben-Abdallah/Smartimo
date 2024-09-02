from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from core.models import Notification, Property, User, TimeStampedModel
from property_listing.models import PropertyOwner


class PropertyTaxInfo(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    assessment_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    tax_breakdown = models.JSONField(blank=True, null=True)
    historical_payments = models.JSONField(blank=True, null=True)

    def retrieve_tax_info(self):
        self.assessment_value = 250000.00
        self.tax_rate = 1.25
        self.due_date = date(2024, 12, 31)
        self.tax_breakdown = {
            "land_tax": 1500.00,
            "building_tax": 1750.00,
            "special_assessments": 250.00
        }
        self.historical_payments = [
            {"date": "2023-12-31", "amount": 3500.00},
            {"date": "2022-12-31", "amount": 3450.00},
        ]
        self.save()

    def update_tax_info(self, property, new_assessment_value, new_tax_rate, new_due_date):
        self.property = property
        self.assessment_value = new_assessment_value
        self.tax_rate = new_tax_rate
        self.due_date = new_due_date
        self.save()

    def get_tax_details(self):
        return {
            "proprty": self.property.property_id,
            "assessment_value": self.assessment_value,
            "tax_rate": self.tax_rate,
            "due_date": self.due_date,
            "tax_breakdown": self.tax_breakdown,
            "historical_payments": self.historical_payments,
        }

    def send_due_date_notifications(self):
        if self.due_date:
            if self.due_date - date.today() <= timedelta(days=30):
                Notification.send_notification(
                    user=User.user_id, 
                    message=f"Your property tax for {self.property.address} is due on {self.due_date}."
                )


class TaxEstimator(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    assessed_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    exemptions = models.JSONField(blank=True, null=True)
    estimated_tax = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def calculate_estimated_tax(self):
        exemption_total = sum([e['amount'] for e in self.exemptions])
        self.estimated_tax = (self.assessed_value * self.tax_rate / 100) - exemption_total
        self.save()

    def adjust_tax_parameters(self, new_property=None, new_assessed_value=None, new_tax_rate=None, new_exemptions=None):
        if new_property:
            self.property.property_id = new_property
        if new_assessed_value:
            self.assessed_value = new_assessed_value
        if new_tax_rate:
            self.tax_rate = new_tax_rate
        if new_exemptions:
            self.exemptions = new_exemptions
        self.calculate_estimated_tax()

    def generate_tax_projection(self):
        return {
            "projected_tax": self.estimated_tax,
            "assessed_value": self.assessed_value,
            "tax_rate": self.tax_rate,
            "exemptions": self.exemptions,
        }

    def save_estimation(self):
        self.save()


class TaxPaymentRecord(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    payment_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=100, choices=[('check', 'Check'), ('electronic_transfer', 'Electronic Transfer')], default='check')
    transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    receipt_url = models.URLField(blank=True, null=True)

    def log_payment(self):
        self.save()

    def get_payment_history(self):
        return {
            "property": self.property.property_id,
            "payment_history": list(
                TaxPaymentRecord.objects.filter(property=self.property.property_id).values()
            ),
        }

    def download_receipt(self):
        return self.receipt_url

    def reconcile_payments(self):
        tax_info = PropertyTaxInfo.objects.get(property=self.property.property_id)
        total_paid = sum([p['amount'] for p in self.get_payment_history()['payment_history']])
        if total_paid != tax_info.assessment_value * tax_info.tax_rate / 100:
            raise ValidationError("Payment reconciliation failed: discrepancy found.")
        else:
            return "Payments reconciled successfully."


class TaxExemptionApplication(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    exemption_type = models.CharField(max_length=255, blank=True, null=True)
    application_status = models.CharField(max_length=100, choices=[('pending', '¨Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    supporting_documents = models.JSONField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    approval_date = models.DateField(null=True, blank=True)

    def apply_for_exemption(self):
        self.application_status = "pending"
        self.submission_date = date.today()
        self.save()

    def upload_documents(self, documents):
        self.supporting_documents = documents
        self.save()

    def track_application_status(self):
        return self.application_status

    def notify_application_outcome(self):
        if self.application_status == "approved":
            Notification.send_notification(
                user=self.owner.user_id,
                message=f"Your application for {self.exemption_type} exemption has been approved."
            )
        elif self.application_status == "rejected":
            Notification.send_notification(
                user=self.owner.user_id,
                message=f"Your application for {self.exemption_type} exemption has been rejected."
            )


class TaxAlertNotification(Notification):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=100, choices=[('assessment-change', 'Assessment Change'), ('policy_update', 'Policy Update')], default='assessment change')
    read_status = models.BooleanField(default=False, blank=True, null=True)

    def send_alert(self, message):
        Notification.send_notification(
            user=User.user_id,
            message=message
        )
        self.save()

    def get_alerts(self):
        return list(TaxAlertNotification.objects.filter(property=self.property.property_id).values())

    def mark_as_read(self):
        self.read_status = True
        self.save()

    def analyze_tax_impact(self):
        return {
            "impact": "Increase in assessment value by 10% will result in a 12% increase in tax liability.",
        }

