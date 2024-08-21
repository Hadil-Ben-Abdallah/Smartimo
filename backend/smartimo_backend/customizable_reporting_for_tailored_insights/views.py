from ninja import Router
from django.shortcuts import get_object_or_404
from .models import (
    CustomizableFinancialReport, SalesReport, MaintenanceReport, InvestmentReport, ComplianceReport
)
from .schemas import (
    CustomizableFinancialReportSchema, SalesReportSchema, MaintenanceReportSchema,
    InvestmentReportSchema, ComplianceReportSchema
)

router = Router()


# Customizable Financial Report
@router.post('/financial-report/', response=CustomizableFinancialReportSchema)
def create_financial_report(request, data: CustomizableFinancialReportSchema):
    report = CustomizableFinancialReport(**data.dict(exclude={'id'}))
    report.save()
    return report


@router.get('/financial-report/{report_id}', response=CustomizableFinancialReportSchema)
def get_financial_report(request, report_id: int):
    report = get_object_or_404(CustomizableFinancialReport, id=report_id)
    return report


@router.put('/financial-report/{report_id}', response=CustomizableFinancialReportSchema)
def update_financial_report(request, report_id: int, data: CustomizableFinancialReportSchema):
    report = get_object_or_404(CustomizableFinancialReport, id=report_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(report, key, value)
    report.save()
    return report


@router.delete('/financial-report/{report_id}')
def delete_financial_report(request, report_id: int):
    report = get_object_or_404(CustomizableFinancialReport, id=report_id)
    report.delete()
    return {"success": True}


# Sales Report
@router.post('/sales-report/', response=SalesReportSchema)
def create_sales_report(request, data: SalesReportSchema):
    report = SalesReport(**data.dict(exclude={'id'}))
    report.save()
    return report


@router.get('/sales-report/{report_id}', response=SalesReportSchema)
def get_sales_report(request, report_id: int):
    report = get_object_or_404(SalesReport, id=report_id)
    return report


@router.put('/sales-report/{report_id}', response=SalesReportSchema)
def update_sales_report(request, report_id: int, data: SalesReportSchema):
    report = get_object_or_404(SalesReport, id=report_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(report, key, value)
    report.save()
    return report


@router.delete('/sales-report/{report_id}')
def delete_sales_report(request, report_id: int):
    report = get_object_or_404(SalesReport, id=report_id)
    report.delete()
    return {"success": True}


# Maintenance Report
@router.post('/maintenance-report/', response=MaintenanceReportSchema)
def create_maintenance_report(request, data: MaintenanceReportSchema):
    report = MaintenanceReport(**data.dict(exclude={'id'}))
    report.save()
    return report


@router.get('/maintenance-report/{report_id}', response=MaintenanceReportSchema)
def get_maintenance_report(request, report_id: int):
    report = get_object_or_404(MaintenanceReport, id=report_id)
    return report


@router.put('/maintenance-report/{report_id}', response=MaintenanceReportSchema)
def update_maintenance_report(request, report_id: int, data: MaintenanceReportSchema):
    report = get_object_or_404(MaintenanceReport, id=report_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(report, key, value)
    report.save()
    return report


@router.delete('/maintenance-report/{report_id}')
def delete_maintenance_report(request, report_id: int):
    report = get_object_or_404(MaintenanceReport, id=report_id)
    report.delete()
    return {"success": True}


# Investment Report
@router.post('/investment-report/', response=InvestmentReportSchema)
def create_investment_report(request, data: InvestmentReportSchema):
    report = InvestmentReport(**data.dict(exclude={'id'}))
    report.save()
    return report


@router.get('/investment-report/{report_id}', response=InvestmentReportSchema)
def get_investment_report(request, report_id: int):
    report = get_object_or_404(InvestmentReport, id=report_id)
    return report


@router.put('/investment-report/{report_id}', response=InvestmentReportSchema)
def update_investment_report(request, report_id: int, data: InvestmentReportSchema):
    report = get_object_or_404(InvestmentReport, id=report_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(report, key, value)
    report.save()
    return report


@router.delete('/investment-report/{report_id}')
def delete_investment_report(request, report_id: int):
    report = get_object_or_404(InvestmentReport, id=report_id)
    report.delete()
    return {"success": True}


# Compliance Report
@router.post('/compliance-report/', response=ComplianceReportSchema)
def create_compliance_report(request, data: ComplianceReportSchema):
    report = ComplianceReport(**data.dict(exclude={'id'}))
    report.save()
    return report


@router.get('/compliance-report/{report_id}', response=ComplianceReportSchema)
def get_compliance_report(request, report_id: int):
    report = get_object_or_404(ComplianceReport, id=report_id)
    return report


@router.put('/compliance-report/{report_id}', response=ComplianceReportSchema)
def update_compliance_report(request, report_id: int, data: ComplianceReportSchema):
    report = get_object_or_404(ComplianceReport, id=report_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(report, key, value)
    report.save()
    return report


@router.delete('/compliance-report/{report_id}')
def delete_compliance_report(request, report_id: int):
    report = get_object_or_404(ComplianceReport, id=report_id)
    report.delete()
    return {"success": True}

