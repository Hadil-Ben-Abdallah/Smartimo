from pydantic import BaseModel
from typing import Optional
from core.schemas import NotificationSchema, ResourceSchema, PortalSchema

class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True
        populate_by_name = True

class UpdatePreferencesSchema(BaseModel):
    frequency: Optional[str]
    delivery_method: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True

class AccessResourceSchema(BaseModel):
    resource_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class TenantPortalSchema(PortalSchema):
    tenant_id: str

    class Config:
        from_attributes = True
        populate_by_name = True

class TenantNotificationSchema(NotificationSchema):
    tenant_id: int
    type: str
    delivery_method: str
    frequency: str

    class Config:
        from_attributes = True
        populate_by_name = True

class TenantResourceSchema(ResourceSchema):
    tenant_id: int

    class Config:
        from_attributes = True
        populate_by_name = True
