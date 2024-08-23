from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date
from core.schemas import UserSchema, ReportSchema

class ProjectSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str
    location: str
    budget: float
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    expected_return: float
    status:str
    inspection_reports: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

class InspectorSchema(UserSchema):
    certifications: dict
    assigned_projects_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class SecurityDeviceSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    device_type: str
    status: str
    last_maintenance_date: date

    class Config:
        from_attributes = True
        populate_by_name = True

class MaintenanceDeviceSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    device_type: str
    status: str
    last_maintenance_date: date
    performance_metrics: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

# class TenantMaintenanceRequestSchema(BaseModel):
#     id: Optional[int] = Field(default=None, alias='id')
#     tenant_id: int
#     property_id: int
#     description: str
#     status: str
#     attachments: Dict

#     class Config:
#         from_attributes = True
#         populate_by_name = True

class InspectionReportSchema(ReportSchema):
    inspector_id: int
    property_id: int
    findings: str
    compliance_status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class ConstructionMonitoringSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    project_id: int
    property_id: int
    camera_feeds: Dict
    progress_photos: Dict
    safety_compliance_checklists: List[dict]

    class Config:
        from_attributes = True
        populate_by_name = True
