from ninja import Router
from .models import SecurityDevice, MaintenanceDevice, InspectionReport, ConstructionMonitoring, Project, Inspector
from .schemas import SecurityDeviceSchema, MaintenanceDeviceSchema,InspectionReportSchema, ConstructionMonitoringSchema, ProjectSchema, InspectorSchema

router = Router()

# Security Device Endpoints
@router.post("/security-device/create", response=SecurityDeviceSchema)
def create_security_device(request, payload: SecurityDeviceSchema):
    device = SecurityDevice.objects.create(**payload.dict(exclude={'id'}))
    return device

@router.get("/security-device/{device_id}", response=SecurityDeviceSchema)
def get_security_device(request, device_id: int):
    device = SecurityDevice.objects.get(id=device_id)
    return device

@router.put("/security-device/update/{device_id}", response=SecurityDeviceSchema)
def update_security_device(request, device_id: int, payload: SecurityDeviceSchema):
    device = SecurityDevice.objects.get(id=device_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(device, key, value)
    device.save()
    return device

# Maintenance Device Endpoints
@router.post("/maintenance-device/create", response=MaintenanceDeviceSchema)
def create_maintenance_device(request, payload: MaintenanceDeviceSchema):
    device = MaintenanceDevice.objects.create(**payload.dict(exclude={'id'}))
    return device

@router.get("/maintenance-device/{device_id}", response=MaintenanceDeviceSchema)
def get_maintenance_device(request, device_id: int):
    device = MaintenanceDevice.objects.get(id=device_id)
    return device

@router.put("/maintenance-device/update/{device_id}", response=MaintenanceDeviceSchema)
def update_maintenance_device(request, device_id: int, payload: MaintenanceDeviceSchema):
    device = MaintenanceDevice.objects.get(id=device_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(device, key, value)
    device.save()
    return device

# Tenant Maintenance Request Endpoints
# @router.post("/tenant-maintenance-request/submit", response=TenantMaintenanceRequestSchema)
# def submit_tenant_maintenance_request(request, payload: TenantMaintenanceRequestSchema):
#     request_obj = TenantMaintenanceRequest.objects.create(**payload.dict(exclude={'id'}))
#     return request_obj

# @router.get("/tenant-maintenance-request/{request_id}", response=TenantMaintenanceRequestSchema)
# def get_tenant_maintenance_request(request, request_id: int):
#     request_obj = TenantMaintenanceRequest.objects.get(id=request_id)
#     return request_obj

# @router.put("/tenant-maintenance-request/update-status/{request_id}", response=TenantMaintenanceRequestSchema)
# def update_tenant_maintenance_request_status(request, request_id: int, payload: TenantMaintenanceRequestSchema):
#     request_obj = TenantMaintenanceRequest.objects.get(id=request_id)
#     for key, value in payload.dict().items():
#         if key != 'id':
#             setattr(request_obj, key, value)
#     request_obj.save()
#     return request_obj

# Inspection Report Endpoints
@router.post("/inspection-report/create", response=InspectionReportSchema)
def create_inspection_report(request, payload: InspectionReportSchema):
    report_obj = InspectionReport.objects.create(**payload.dict(exclude={'id'}))
    return report_obj

@router.get("/inspection-report/{report_id}", response=InspectionReportSchema)
def get_inspection_report(request, report_id: int):
    report_obj = InspectionReport.objects.get(id=report_id)
    return report_obj

@router.put("/inspection-report/update/{report_id}", response=InspectionReportSchema)
def update_inspection_report(request, report_id: int, payload: InspectionReportSchema):
    report_obj = InspectionReport.objects.get(id=report_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(report_obj, key, value)
    report_obj.save()
    return report_obj

# Construction Monitoring Endpoints
@router.post("/construction-monitoring/start", response=ConstructionMonitoringSchema)
def start_construction_monitoring(request, payload: ConstructionMonitoringSchema):
    monitoring_obj = ConstructionMonitoring.objects.create(**payload.dict(exclude={'id'}))
    return monitoring_obj

@router.get("/construction-monitoring/{monitoring_id}", response=ConstructionMonitoringSchema)
def get_construction_monitoring(request, monitoring_id: int):
    monitoring_obj = ConstructionMonitoring.objects.get(id=monitoring_id)
    return monitoring_obj

@router.put("/construction-monitoring/update/{monitoring_id}", response=ConstructionMonitoringSchema)
def update_construction_monitoring(request, monitoring_id: int, payload:ConstructionMonitoringSchema):
    monitoring_obj = ConstructionMonitoring.objects.get(id=monitoring_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(monitoring_obj, key, value)
    monitoring_obj.save()
    return monitoring_obj

# Project Endpoints
@router.post("/project/create", response=ProjectSchema)
def create_project(request, payload: ProjectSchema):
    project_obj = Project.objects.create(**payload.dict(exclude={'id'}))
    return project_obj

@router.get("/project/{project_id}", response=ProjectSchema)
def get_project(request, project_id: int):
    project_obj = Project.objects.get(id=project_id)
    return project_obj

@router.put("/project/update/{project_id}", response=ProjectSchema)
def update_project(request, project_id: int, payload: ProjectSchema):
    project_obj = Project.objects.get(id=project_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(project_obj, key, value)
    project_obj.save()
    return project_obj

# Inspector Endpoints
@router.post("/inspector/assign", response=InspectorSchema)
def assign_inspector(request, payload: InspectorSchema):
    inspector_obj = Inspector.objects.create(**payload.dict(exclude={'id'}))
    return inspector_obj

@router.get("/inspector/{inspector_id}", response=InspectorSchema)
def get_inspector(request, inspector_id: int):
    inspector_obj = Inspector.objects.get(id=inspector_id)
    return inspector_obj

@router.put("/inspector/update/{inspector_id}", response=InspectorSchema)
def update_inspector(request, inspector_id: int, payload: InspectorSchema):
    inspector_obj = Inspector.objects.get(id=inspector_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(inspector_obj, key, value)
    inspector_obj.save()
    return inspector_obj
