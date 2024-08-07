from ninja import Router
from .models import MaintenanceRequest, TenantRequest, MaintenancePropertyManager, MaintenanceTechnician, MaintenanceNotification
from .schemas import CreateMaintenanceRequestSchema, UpdateMaintenanceRequestSchema, MaintenanceRequestSchema, TenantRequestSchema, MaintenancePropertyManagerSchema, MaintenanceTechnicianSchema, MaintenanceNotificationSchema
from django.shortcuts import get_object_or_404

router = Router()

@router.post("/maintenance-requests", response=MaintenanceRequestSchema)
def create_maintenance_request(request, payload: CreateMaintenanceRequestSchema):
    maintenance_request = MaintenanceRequest.objects.create(**payload.dict(exclude={'id'}))
    maintenance_request.submit_request()
    return maintenance_request

@router.put("/maintenance-requests/{request_id}", response=MaintenanceRequestSchema)
def update_maintenance_request(request, request_id: int, payload: UpdateMaintenanceRequestSchema):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=request_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(maintenance_request, attr, value)
    maintenance_request.save()
    return maintenance_request

@router.get("/maintenance-requests/{request_id}", response=MaintenanceRequestSchema)
def get_maintenance_request(request, request_id: int):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=request_id)
    return maintenance_request

@router.post("/tenant-requests", response=TenantRequestSchema)
def create_tenant_request(request, payload: TenantRequestSchema):
    tenant_request = TenantRequest.objects.create(**payload.dict(exclude={'id'}))
    return tenant_request

@router.get("/property-managers/{manager_id}", response=MaintenancePropertyManagerSchema)
def get_property_manager(request, manager_id: int):
    property_manager = get_object_or_404(MaintenancePropertyManager, id=manager_id)
    return property_manager

@router.get("/technicians/{technician_id}", response=MaintenanceTechnicianSchema)
def get_technician(request, technician_id: int):
    technician = get_object_or_404(MaintenanceTechnician, id=technician_id)
    return technician

@router.post("/notifications", response=dict)
def create_notification(request, payload: MaintenanceNotificationSchema):
    notification = MaintenanceNotification.objects.create(**payload.dict(exclude={'id'}))
    return {"status": "Notification created"}


