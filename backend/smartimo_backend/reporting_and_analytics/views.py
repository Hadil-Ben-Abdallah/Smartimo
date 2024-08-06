from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import (
    Report,
    PropertyPerformanceReport,
    SalesTrendReport,
    FinancialPerformanceReport,
    ClientEngagementReport,
    AutomatedReportScheduler
)
from .schemas import (
    ReportSchema,
    PropertyPerformanceReportSchema,
    SalesTrendReportSchema,
    FinancialPerformanceReportSchema,
    ClientEngagementReportSchema,
    AutomatedReportSchedulerSchema
)

router = Router()

@router.get("/reports", response=List[ReportSchema])
def list_reports(request):
    reports = Report.objects.all()
    return reports

@router.post("/reports", response=ReportSchema)
def create_report(request, report: ReportSchema):
    report_data = report.dict(exclude_unset=True)
    report_obj = Report.objects.create(**report_data)
    return report_obj

@router.get("/reports/{report_id}", response=ReportSchema)
def get_report(request, report_id: int):
    report = get_object_or_404(Report, id=report_id)
    return report

@router.post("/reports/{report_id}/generate", response=ReportSchema)
def generate_report(request, report_id: int):
    report = get_object_or_404(Report, id=report_id)
    report.generate_report()
    return report

@router.get("/automated-reports", response=List[AutomatedReportSchedulerSchema])
def list_automated_reports(request):
    automated_reports = AutomatedReportScheduler.objects.all()
    return automated_reports

@router.post("/automated-reports", response=AutomatedReportSchedulerSchema)
def create_automated_report(request, automated_report: AutomatedReportSchedulerSchema):
    automated_report_data = automated_report.dict(exclude_unset=True)
    automated_report_obj = AutomatedReportScheduler.objects.create(**automated_report_data)
    return automated_report_obj

@router.get("/automated-reports/{scheduler_id}", response=AutomatedReportSchedulerSchema)
def get_automated_report(request, scheduler_id: int):
    scheduler = get_object_or_404(AutomatedReportScheduler, id=scheduler_id)
    return scheduler

@router.post("/automated-reports/{scheduler_id}/schedule", response=AutomatedReportSchedulerSchema)
def schedule_automated_report(request, scheduler_id: int):
    scheduler = get_object_or_404(AutomatedReportScheduler, id=scheduler_id)
    scheduler.schedule_report()
    return scheduler

@router.post("/automated-reports/{scheduler_id}/send", response=AutomatedReportSchedulerSchema)
def send_automated_report(request, scheduler_id: int):
    scheduler = get_object_or_404(AutomatedReportScheduler, id=scheduler_id)
    scheduler.send_report()
    return scheduler

@router.put("/automated-reports/{scheduler_id}", response=AutomatedReportSchedulerSchema)
def update_automated_report(request, scheduler_id: int, payload: AutomatedReportSchedulerSchema):
    scheduler = get_object_or_404(AutomatedReportScheduler, id=scheduler_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(scheduler, attr, value)
    scheduler.save()
    return scheduler

@router.delete("/automated-reports/{scheduler_id}", response=dict)
def cancel_automated_report(request, scheduler_id: int):
    scheduler = get_object_or_404(AutomatedReportScheduler, id=scheduler_id)
    scheduler.cancel_schedule()
    return {"success": True}

@router.put("/reports/{report_id}", response=ReportSchema)
def update_report(request, report_id: int, payload: ReportSchema):
    report = get_object_or_404(Report, id=report_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(report, attr, value)
    report.save()
    return report

@router.put("/property-performance-reports/{report_id}", response=PropertyPerformanceReportSchema)
def update_property_performance_report(request, report_id: int, payload: PropertyPerformanceReportSchema):
    report = get_object_or_404(PropertyPerformanceReport, id=report_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(report, attr, value)
    report.save()
    return report

@router.put("/sales-trend-reports/{report_id}", response=SalesTrendReportSchema)
def update_sales_trend_report(request, report_id: int, payload: SalesTrendReportSchema):
    report = get_object_or_404(SalesTrendReport, id=report_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(report, attr, value)
    report.save()
    return report

@router.put("/financial-performance-reports/{report_id}", response=FinancialPerformanceReportSchema)
def update_financial_performance_report(request, report_id: int, payload: FinancialPerformanceReportSchema):
    report = get_object_or_404(FinancialPerformanceReport, id=report_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(report, attr, value)
    report.save()
    return report

@router.put("/client-engagement-reports/{report_id}", response=ClientEngagementReportSchema)
def update_client_engagement_report(request, report_id: int, payload: ClientEngagementReportSchema):
    report = get_object_or_404(ClientEngagementReport, id=report_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(report, attr, value)
    report.save()
    return report

