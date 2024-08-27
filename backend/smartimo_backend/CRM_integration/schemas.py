from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CRMIntegrationSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    crm_tool: str
    api_key: str
    sync_status: str
    last_sync_time: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class CRMClientSyncSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    client: int
    crm_client_id: str
    sync_status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CRMSalesOpportunitySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    crm_opportunity_id: str
    property: int
    stage: str
    value: float
    probability: float

    class Config:
        from_attributes = True
        populate_by_name = True

class CRMClientInteractionSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    client: int
    interaction_type: str
    details: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CRMClientSegmentationSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    segment_name: str
    criteria: str
    client_list: List[int]

    class Config:
        from_attributes = True
        populate_by_name = True

class CRMIntegrationSettingsSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    crm_tool: str
    custom_fields: dict
    sync_frequency: str
    notification_settings: dict

    class Config:
        from_attributes = True
        populate_by_name = True
