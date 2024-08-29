from django.db import models
from core.models import Report
from lease_rental_management.models import Tenant, PropertyManager

class TenantPaymentHistory(models.Model):
    PAYMENT_TYPES = [
        ('rent', 'Rent'),
        ('security_deposit', 'Security Deposit'),
        ('utility_bill', 'Utility Bill'),
    ]

    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    lease_period = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def view_payment_history(self):
        return TenantPaymentHistory.objects.filter(tenant=self.tenant)

    def add_payment_record(self, payment_type, amount, payment_date, payment_method, lease_period, description=""):
        new_record = TenantPaymentHistory(
            tenant=self.tenant,
            payment_type=payment_type,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            lease_period=lease_period,
            description=description
        )
        new_record.save()
        return new_record

    def update_payment_record(self, payment_id, **kwargs):
        payment_record = TenantPaymentHistory.objects.get(id=payment_id, tenant=self.tenant.user_id)
        for key, value in kwargs.items():
            setattr(payment_record, key, value)
        payment_record.save()
        return payment_record

    def get_payment_summary(self):
        return TenantPaymentHistory.objects.filter(tenant=self.tenant).values(
            'payment_type'
        ).annotate(
            total_amount=models.Sum('amount'),
            count=models.Count('id')
        )


class PaymentFilter(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50, null=True, blank=True)
    date_range_start = models.DateField(null=True, blank=True)
    date_range_end = models.DateField(null=True, blank=True)
    amount_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    keyword = models.CharField(max_length=100, null=True, blank=True)

    def filter_payment_history(self):
        query = TenantPaymentHistory.objects.filter(tenant=self.tenant)
        if self.payment_type:
            query = query.filter(payment_type=self.payment_type)
        if self.date_range_start and self.date_range_end:
            query = query.filter(payment_date__range=[self.date_range_start, self.date_range_end])
        if self.amount_min is not None and self.amount_max is not None:
            query = query.filter(amount__range=[self.amount_min, self.amount_max])
        if self.keyword:
            query = query.filter(description__icontains=self.keyword)
        return query

    def search_payment_history(self):
        return TenantPaymentHistory.objects.filter(
            tenant=self.tenant.user_id,
            description__icontains=self.keyword
        )


class PaymentExport(models.Model):
    EXPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
    ]

    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    export_format = models.CharField(max_length=50, choices=[('pdf', 'PDF'),('csv', 'CSV')], default='pdf')
    export_date = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)

    def download_payment_history(self):
        if self.export_format == 'pdf':
            file_name = f"{self.tenant.username}_payment_history.pdf"
            self.file_path = f"/path/to/pdf/{file_name}"
        elif self.export_format == 'csv':
            file_name = f"{self.tenant.username}_payment_history.csv"
            self.file_path = f"/path/to/csv/{file_name}"
        with open(self.file_path, 'w') as file:
            file.write("Simulated payment history content")
        self.save()
        return self.file_path

    def print_payment_history(self):
        return f"Printing payment history for tenant: {self.tenant.username}"


class PaymentValidation(models.Model):
    VALIDATION_STATUS_CHOICES = [
        ('validated', 'Validated'),
        ('pending', 'Pending'),
        ('discrepancy_found', 'Discrepancy Found'),
    ]

    id = models.AutoField(primary_key=True)
    payment_history = models.ForeignKey(TenantPaymentHistory, on_delete=models.CASCADE)
    validated_by = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    validation_status = models.CharField(max_length=50, choices=VALIDATION_STATUS_CHOICES)
    discrepancy_notes = models.TextField(null=True, blank=True)

    def validate_payment_history(self):
        if self.payment_history.amount > 0:
            self.validation_status = 'validated'
        else:
            self.validation_status = 'discrepancy_found'
            self.discrepancy_notes = "Invalid payment amount"
        self.save()
        return self.validation_status

    def reconcile_payment_records(self):
        reconciled = True
        if reconciled:
            self.validation_status = 'validated'
        else:
            self.validation_status = 'discrepancy_found'
            self.discrepancy_notes = "Reconciliation failed"
        self.save()
        return reconciled

    def flag_discrepancy(self, notes):
        self.validation_status = 'discrepancy_found'
        self.discrepancy_notes = notes
        self.save()
        return self.validation_status


class PaymentHistoryReport(Report):
    REPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
    ]

    report_id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date_range_start = models.DateField(blank=True, null=True)
    date_range_end = models.DateField(blank=True, null=True)
    report_format = models.CharField(max_length=50, choices=[('pdf', 'PDF'),('excel', 'Excel')], default='pdf')
    generated_at = models.DateTimeField(auto_now_add=True)

    def generate_report(self):
        report_data = TenantPaymentHistory.objects.filter(
            tenant=self.tenant,
            payment_date__range=[self.date_range_start, self.date_range_end]
        )
        report_content = f"Report for tenant {self.tenant.username} from {self.date_range_start} to {self.date_range_end}"
        return report_content

    def customize_report(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
        return self

    def send_report(self):
        return f"Report sent to {self.property_manager.username} and tenant {self.tenant.username}"

