from ninja import Router
from django.shortcuts import get_object_or_404
from .models import IntegrationSettings, IntegrationFinancialReport, Reconciliation, Export
from .schemas import IntegrationSettingsSchema, IntegrationFinancialReportSchema, ReconciliationSchema, ExportSchema

router = Router()

@router.post("/settings/", response=IntegrationSettingsSchema)
def create_integration_settings(request, data: IntegrationSettingsSchema):
    settings = IntegrationSettings.objects.create(**data.dict(exclude={'id'}))
    return settings

@router.put("/settings/{integration_id}/", response=IntegrationSettingsSchema)
def update_integration_settings(request, integration_id: int, data: IntegrationSettingsSchema):
    settings = get_object_or_404(IntegrationSettings, integration_id=integration_id)
    payload = data.dict()
    for key, value in payload.items():
        if key != 'id':
            setattr(settings, key, value)
    settings.save()
    return settings

@router.post("/reports/", response=IntegrationFinancialReportSchema)
def generate_financial_report(request, data: IntegrationFinancialReportSchema):
    report = IntegrationFinancialReport.objects.create(**data.dict(exclude={'id'}))
    return report

@router.post("/reconciliation/", response=ReconciliationSchema)
def start_reconciliation(request, data: ReconciliationSchema):
    reconciliation = Reconciliation.objects.create(**data.dict(exclude={'id'}))
    reconciliation.start_reconciliation()
    return reconciliation

@router.post("/exports/", response=ExportSchema)
def initiate_export(request, data: ExportSchema):
    export = Export.objects.create(**data.dict(exclude={'id'}))
    export.initiate_export()
    return export
