from ninja import Router, File, UploadedFile
from .models import (OwnerPortal, OwnerFinancialReport, PerformanceMetric, 
                    OwnerNotification, PortalCommunication, OwnerResource)
from .schemas import (OwnerPortalSchema, OwnerFinancialReportSchema, 
                      PerformanceMetricSchema, OwnerNotificationSchema, 
                      PortalCommunicationSchema, OwnerResourceSchema)
from django.shortcuts import get_object_or_404
from typing import List

router = Router()

# OwnerPortal Endpoints
@router.post("/owner-portals/", response=OwnerPortalSchema)
def create_owner_portal(request, payload: OwnerPortalSchema):
    data = payload.dict(exclude={'id'})
    portal = OwnerPortal.objects.create(**data)
    return portal

# OwnerFinancialReport Endpoints
@router.post("/financial-reports/", response=OwnerFinancialReportSchema)
def create_financial_report(request, payload: OwnerFinancialReportSchema):
    data = payload.dict(exclude={'id'})
    report = OwnerFinancialReport.objects.create(**data)
    return report

@router.get("/financial-reports/{report_id}", response=OwnerFinancialReportSchema)
def view_financial_report(request, report_id: int):
    report = get_object_or_404(OwnerFinancialReport, id=report_id)
    return report

# PerformanceMetric Endpoints
@router.post("/performance-metrics/", response=PerformanceMetricSchema)
def create_performance_metric(request, payload: PerformanceMetricSchema):
    data = payload.dict(exclude={'performance_id'})
    metric = PerformanceMetric.objects.create(**data)
    return metric

@router.get("/performance-metrics/{metric_id}", response=PerformanceMetricSchema)
def view_performance_metric(request, metric_id: int):
    metric = get_object_or_404(PerformanceMetric, performance_id=metric_id)
    return metric

# OwnerNotification Endpoints
@router.post("/owner-notifications/", response=OwnerNotificationSchema)
def create_owner_notification(request, payload: OwnerNotificationSchema):
    data = payload.dict(exclude={'id'})
    notification = OwnerNotification.objects.create(**data)
    return notification

@router.put("/owner-notifications/{notification_id}", response=OwnerNotificationSchema)
def update_owner_notification(request, notification_id: int, payload: OwnerNotificationSchema):
    notification = get_object_or_404(OwnerNotification, id=notification_id)
    data = payload.dict()
    for key, value in data.items():
        if key != 'id':
            setattr(notification, key, value)
    notification.save()
    return notification

# PortalCommunication Endpoints
@router.post("/portal-communication/", response=PortalCommunicationSchema)
def create_portal_communication(request, payload: PortalCommunicationSchema):
    data = payload.dict(exclude={'id'})
    communication = PortalCommunication.objects.create(**data)
    return communication

@router.put("/portal-communication/{communication_id}", response=PortalCommunicationSchema)
def update_portal_communication(request, communication_id: int, payload: PortalCommunicationSchema):
    communication = get_object_or_404(PortalCommunication, id=communication_id)
    data = payload.dict()
    for key, value in data.items():
        if key != 'id':
            setattr(communication, key, value)
    communication.save()
    return communication

@router.get("/portal-communication/{communication_id}/log", response=PortalCommunicationSchema)
def view_portal_communication_log(request, communication_id: int):
    communication = get_object_or_404(PortalCommunication, id=communication_id)
    return communication.view_log()

@router.post("/portal-communication/{communication_id}/attachments")
def add_attachments_to_communication(request, communication_id: int, files: List[UploadedFile]):
    communication = get_object_or_404(PortalCommunication, id=communication_id)
    communication.attach_files(files)
    return {"detail": "Files attached successfully"}

# OwnerResource Endpoints
@router.post("/owner-resources/", response=OwnerResourceSchema)
def create_owner_resource(request, payload: OwnerResourceSchema):
    data = payload.dict(exclude={'id'})
    resource = OwnerResource.objects.create(**data)
    return resource

@router.put("/owner-resources/{resource_id}", response=OwnerResourceSchema)
def update_owner_resource(request, resource_id: int, payload: OwnerResourceSchema):
    resource = get_object_or_404(OwnerResource, id=resource_id)
    data = payload.dict()
    for key, value in data.items():
        if key != 'id':
            setattr(resource, key, value)
    resource.save()
    return resource

@router.get("/owner-resources/{resource_id}/access")
def access_owner_resource(request, resource_id: int):
    resource = get_object_or_404(OwnerResource, id=resource_id)
    return resource.access_resource()

@router.get("/owner-resources/{resource_id}/download")
def download_template(request, resource_id: int, template_name: str):
    resource = get_object_or_404(OwnerResource, id=resource_id)
    return resource.download_template(template_name)

@router.post("/owner-resources/{resource_id}/consultation")
def request_consultation(request, resource_id: int):
    resource = get_object_or_404(OwnerResource, id=resource_id)
    return resource.request_consultation()
