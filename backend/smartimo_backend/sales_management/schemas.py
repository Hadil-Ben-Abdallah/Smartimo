from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LeadSchema(BaseModel):
    lead_source: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CreateLeadSchema(BaseModel):
    name: str
    email: str
    phone: str
    property_preferences: dict
    lead_source: str
    status: str
    agent_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class UpdateLeadSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    property_preferences: Optional[dict] = None
    lead_source: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class SalesClientInteractionSchema(BaseModel):
    lead_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class TheSalesOpportunitySchema(BaseModel):
    lead_id: int
    property_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class SalesPipelineSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    agent_id: int
    stages: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class CreatePipelineSchema(BaseModel):
    agent_id: int
    stages: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class UpdatePipelineSchema(BaseModel):
    stages: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class CollaborationSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    opportunity_id: int
    agent_id: int
    notes: str
    assigned_tasks: dict
    activity_feed: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class SalesAnalyticsSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    agent_id: int
    metrics: dict
    report_type: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

