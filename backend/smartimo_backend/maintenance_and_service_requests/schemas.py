from pydantic import BaseModel, Field
from typing import List, Optional
from core.schemas import NotificationSchema

class MaintenanceRequestSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    tenant: str
    manager: str
    property: str
    issue_type: str
    severity: str
    location: str
    description: str
    photos: List[str]
    urgency_level: str
    status: str
    submission_date: str
    completion_date: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CreateMaintenanceRequestSchema(BaseModel):
    issue_type: str
    severity: str
    location: str
    description: str
    photos: Optional[List[str]] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class UpdateMaintenanceRequestSchema(BaseModel):
    issue_type: Optional[str] = None
    severity: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    photos: Optional[List[str]] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class TenantRequestSchema(BaseModel):
    tenant_id: str
    unit_number: str
    maintenance_requests: List[int]

    class Config:
        from_attributes = True
        populate_by_name = True

class MaintenancePropertyManagerSchema(BaseModel):
    property_manager_id: str
    assigned_requests: List[int]

    class Config:
        from_attributes = True
        populate_by_name = True

class MaintenanceTechnicianSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str
    email: str
    phone: str
    skills: str
    assigned_tasks: List[int]

    class Config:
        from_attributes = True
        populate_by_name = True

class MaintenanceNotificationSchema(NotificationSchema):
    recipient_id: int
    type: str

    class Config:
        from_attributes = True
        populate_by_name = True
