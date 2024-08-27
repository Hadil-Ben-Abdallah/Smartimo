from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from core.schemas import SalesOpportunitySchema
from client_management.schemas import ClientSchema, InteractionSchema

class LeadSchema(ClientSchema):
    lead_source: str
    lead_status: str
    property_type: str
    note: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CreateLeadSchema(BaseModel):
    name: str
    email: str
    phone: str
    property_preferences: dict
    lead_source: str
    property_type: str
    note: str
    lead_status: str
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
    lead_status: Optional[str] = None
    property_type: Optional[str] = None
    note: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class DealSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    title: str
    property: str
    lead: str
    start_date: datetime
    end_date: datetime
    description: str
    is_approved: bool
    deal_type: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CreateDealSchema(BaseModel):
    title: str
    property: str
    lead: str
    start_date: datetime
    end_date: datetime
    description: str
    is_approved: bool
    deal_type: str

class UpdateDealSchema(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    property: Optional[str] = None
    lead: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    is_approved: Optional[str] = None
    deal_type: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class SalesClientInteractionSchema(InteractionSchema):
    lead_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class TheSalesOpportunitySchema(SalesOpportunitySchema):
    lead_id: int
    property_id: int

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

    class Config:
        from_attributes = True
        populate_by_name = True

