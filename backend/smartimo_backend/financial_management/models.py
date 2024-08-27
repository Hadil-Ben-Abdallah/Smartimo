from django.db import models
from core.models import Property, User, Report
from django.db.models import JSONField
from datetime import datetime
from django.core.mail import send_mail


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid'), ('overdue', 'Overdue')])
    itemized_charges = JSONField()
    payment_instructions = models.TextField()

    def generate_invoice(self):
        self.status = 'unpaid'
        self.save()
        return f"Invoice {self.id} generated for tenant {self.tenant.id}."

    def send_invoice(self):
        subject = f"Invoice #{self.id}"
        message = f"Dear {self.tenant.username},\n\nPlease find your invoice attached.\n\nAmount Due: {self.amount_due}\nDue Date: {self.due_date}\n\nThank you."
        from_email = "smartimo@example.com"
        recipient_list = [self.tenant.email]
        send_mail(subject, message, from_email, recipient_list)
        return f"Invoice {self.id} sent to tenant {self.tenant.id}."

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def get_invoice_details(self):
        return {
            "id": self.id,
            "tenant": self.tenant,
            "property": self.property,
            "amount_due": self.amount_due,
            "due_date": self.due_date,
            "status": self.status,
            "itemized_charges": self.itemized_charges,
            "payment_instructions": self.payment_instructions,
        }

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_card_number = models.CharField(max_length=20)
    reached_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('processed', 'Processed'), ('pending', 'Pending')])

    def record_payment(self):
        self.status = 'processed'
        self.save()
        return f"Payment {self.id} recorded for invoice {self.invoice.id}."

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def get_payment_details(self):
        return {
            "id": self.id,
            "invoice": self.invoice.id,
            "user": self.user,
            "credit_card_number": self.credit_card_number,
            "reached_amount": self.reached_amount,
            "remaining_amount": self.remaining_amount,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "status": self.status,
        }

    def reconcile_payment(self):
        self.invoice.update_status('paid')
        self.update_status('processed')
        return f"Payment {self.id} reconciled for invoice {self.invoice.id}."

class FinancialReport(Report):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    report_period = models.CharField(max_length=50)

    def generate_report(self):
        report_content = f"Report Type: {self.report_type}\nPeriod: {self.report_period}\nProperty: {self.property.address}"
        return report_content

    def customize_report(self, params):
        return f"Financial report {self} customized with params {params}."

    def export_report(self, format):
        report_content = self.generate_report()
        if format == "PDF":
            exported_content = f"PDF: {report_content}"
        elif format == "Excel":
            exported_content = f"Excel: {report_content}"
        else:
            exported_content = report_content
        return exported_content

    def schedule_report_delivery(self, schedule):
        return f"Financial report {self} scheduled for delivery on {schedule}."

class FinancialTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    description = models.TextField()

    def record_transaction(self):
        self.save()
        return f"Transaction {self.id} recorded for property {self.property}."

    def get_transaction_details(self):
        return {
            "id": self.id,
            "property": self.property,
            "transaction_date": self.transaction_date,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "description": self.description,
        }

    def update_transaction(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return f"Transaction {self.id} updated."

class FinancialPortal(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    invoices = models.ManyToManyField(Invoice)
    payment_history = models.ManyToManyField(Payment)

    def view_invoice(self, invoice_id):
        return self.invoices.get(id=invoice_id)

    def view_payment_history(self):
        return self.payment_history.all()

    def download_invoice(self, invoice_id):
        invoice = self.view_invoice(invoice_id)
        return f"Invoice {invoice.id} downloaded."

    def make_payment(self, invoice_id, amount):
        invoice = self.view_invoice(invoice_id)
        payment = Payment.objects.create(
            invoice=invoice,
            user=self.tenant,
            amount_paid=amount,
            payment_date=datetime.now().date(),
            payment_method="Online",
            status="pending"
        )
        return payment.record_payment()
