from django.db import models
from django.utils import timezone
from vendor_management.models import Vendor, Contract
from core.models import TimeStampedModel

class VendorInvoice(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('paid', 'Paid')], default='pending')
    captured_data = models.JSONField(blank=True, null=True)

    def capture_invoice(self, data):
        self.invoice_number = data.get('invoice_number')
        self.invoice_date = data.get('invoice_date')
        self.amount = data.get('amount')
        self.captured_data = data
        self.save()

    def verify_invoice(self):
        if not self.invoice_number or not self.invoice_date or self.amount <= 0:
            raise ValueError("Invoice data is incomplete or incorrect")
        return True

    def update_status(self, new_status):
        if new_status in ['pending', 'approved', 'paid']:
            self.status = new_status
            self.save()
        else:
            raise ValueError("Invalid status")

class ApprovalWorkflow(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(VendorInvoice, on_delete=models.CASCADE)
    rules = models.JSONField(blank=True, null=True)
    approval_levels = models.JSONField(blank=True, null=True)
    escalation_procedures = models.JSONField(blank=True, null=True)
    current_stage = models.CharField(max_length=100, blank=True, null=True)

    def configure_workflow(self, rules, approval_levels):
        self.rules = rules
        self.approval_levels = approval_levels
        self.save()

    def trigger_approval(self):
        if not self.rules or not self.approval_levels:
            raise ValueError("Approval rules or levels are not configured")
        self.current_stage = 'pending_approval'
        self.save()

    def escalate_invoice(self):
        if self.current_stage == 'pending_approval':
            self.current_stage = 'escalated'
            self.save()
        else:
            raise ValueError("Cannot escalate at this stage")

    def approve_invoice(self):
        if self.current_stage != 'pending_approval':
            raise ValueError("Invoice cannot be approved at this stage")
        self.invoice.update_status('approved')
        self.current_stage = 'completed'
        self.save()

class InvoiceTrackingDashboard(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey('PropertyManager', on_delete=models.CASCADE)
    invoices = models.ManyToManyField(VendorInvoice)
    filters = models.JSONField(blank=True, null=True)

    def track_invoice(self, invoice_id):
        invoice = VendorInvoice.objects.get(id=invoice_id)
        self.invoices.add(invoice)

    def filter_invoices(self, criteria):
        filtered_invoices = VendorInvoice.objects.all()
        for key, value in criteria.items():
            if hasattr(VendorInvoice, key):
                filtered_invoices = filtered_invoices.filter(**{key: value})
        return filtered_invoices

    def send_notifications(self):
        overdue_invoices = self.invoices.filter(status='pending').filter(invoice_date__lt=timezone.now().date())
        for invoice in overdue_invoices:
            print(f"Notification: Invoice {invoice.invoice_number} is overdue.")

    def get_invoice_status(self, invoice_id):
        invoice = VendorInvoice.objects.get(id=invoice_id)
        return invoice.status

class ContractReconciliation(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(VendorInvoice, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    matched_items = models.JSONField(blank=True, null=True)
    discrepancies = models.JSONField(blank=True, null=True)

    def match_invoice_to_contract(self):
        invoice_items = self.invoice.captured_data.get('items', [])
        contract_scope = self.contract.scope_of_work

        matched_items = [item for item in invoice_items if item in contract_scope]
        self.matched_items = matched_items
        self.save()

    def identify_discrepancies(self):
        invoice_items = self.invoice.captured_data.get('items', [])
        contract_scope = self.contract.scope_of_work

        discrepancies = [item for item in invoice_items if item not in contract_scope]
        self.discrepancies = discrepancies
        self.save()

    def reconcile_discrepancies(self):
        if not self.discrepancies:
            return "No discrepancies found."
        for discrepancy in self.discrepancies:
            print(f"Discrepancy: {discrepancy}")
        return "Discrepancies reconciled."

    def dispute_invoice(self):
        if self.discrepancies:
            self.invoice.update_status('disputed')
            return "Invoice disputed"
        else:
            return "No discrepancies to dispute"

class PaymentProcessing(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(VendorInvoice, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[('electronic', 'Electronic'), ('check', 'Check'), ('wire_transfer', 'Wire Transfer')], default='electronic')
    payment_date = models.DateField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    confirmation_receipt = models.TextField(blank=True, null=True)

    def initiate_payment(self, method):
        if method not in ['electronic', 'check', 'wire_transfer']:
            raise ValueError("Invalid payment method")
        self.payment_method = method
        self.payment_date = timezone.now().date()
        self.payment_status = 'pending'
        self.save()

    def process_batch_payment(self, invoices):
        for invoice_id in invoices:
            invoice = VendorInvoice.objects.get(id=invoice_id)
            if invoice.status == 'approved':
                payment = PaymentProcessing(invoice=invoice, payment_method=self.payment_method)
                payment.initiate_payment(self.payment_method, schedule=None)
                payment.payment_status = 'completed'
                payment.save()

    def generate_receipt(self):
        return f"Receipt for payment {self.id}: {self.confirmation_receipt}"

    def update_payment_status(self, new_status):
        if new_status not in ['pending', 'completed']:
            raise ValueError("Invalid payment status")
        self.payment_status = new_status
        self.save()

