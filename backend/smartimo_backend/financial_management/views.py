from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Invoice, Payment, TheFinancialReport, FinancialTransaction, TenantPortal
from .schemas import InvoiceSchema, PaymentSchema, TheFinancialReportSchema, FinancialTransactionSchema, TenantPortalSchema

router = Router()

@router.post("/invoices/", response=InvoiceSchema)
def create_invoice(request, payload: InvoiceSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    invoice = Invoice.objects.create(**payload_dict)
    return invoice

@router.put("/invoices/{invoice_id}/", response=InvoiceSchema)
def update_invoice(request, invoice_id: int, payload: InvoiceSchema):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(invoice, attr, value)
    invoice.save()
    return invoice


@router.post("/payments/", response=PaymentSchema)
def create_payment(request, payload: PaymentSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    payment = Payment.objects.create(**payload_dict)
    return payment

@router.put("/payments/{payment_id}/", response=PaymentSchema)
def update_payment(request, payment_id: int, payload: PaymentSchema):
    payment = get_object_or_404(Payment, id=payment_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(payment, attr, value)
    payment.save()
    return payment


@router.post("/transactions/", response=FinancialTransactionSchema)
def create_transaction(request, payload: FinancialTransactionSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    transaction = FinancialTransaction.objects.create(**payload_dict)
    return transaction

@router.put("/transactions/{transaction_id}/", response=FinancialTransactionSchema)
def update_transaction(request, transaction_id: int, payload: FinancialTransactionSchema):
    transaction = get_object_or_404(FinancialTransaction, id=transaction_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(transaction, attr, value)
    transaction.save()
    return transaction


@router.post("/financial-reports/", response=TheFinancialReportSchema)
def create_financial_report(request, payload: TheFinancialReportSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    financial_report = TheFinancialReport.objects.create(**payload_dict)
    return financial_report

@router.put("/financial-reports/{report_id}/", response=TheFinancialReportSchema)
def update_financial_report(request, report_id: int, payload: TheFinancialReportSchema):
    financial_report = get_object_or_404(TheFinancialReport, id=report_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(financial_report, attr, value)
    financial_report.save()
    return financial_report


@router.get("/tenant-portal/{tenant_id}/", response=TenantPortalSchema)
def get_tenant_portal(request, tenant_id: int):
    tenant_portal = get_object_or_404(TenantPortal, tenant_id=tenant_id)
    return tenant_portal


