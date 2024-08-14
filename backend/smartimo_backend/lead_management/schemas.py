from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from core.schemas import CommunicationSchema

class LeadCaptureFormSchema(BaseModel):
    form_id: Optional[int] = Field(default=None, alias='id')
    form_fields: List[str]
    form_url: HttpUrl
    customization_options: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class SocialMediaLeadSchema(BaseModel):
    lead_id: int
    platform: str
    campaign_id: str
    ad_creative: str
    engagement_metrics: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class OfflineLeadSchema(BaseModel):
    lead_id: int
    source: str
    event_details: str
    contact_information: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class LeadAssignmentSchema(BaseModel):
    assignment_id: Optional[int] = Field(default=None, alias='id')
    lead_id: int
    agent_id: int
    criteria: dict
    assignment_date: str

    class Config:
        from_attributes = True
        populate_by_name = True

class LeadCommunicationSchema(CommunicationSchema):
    lead_id: int
    agent_id: int
    communication_type: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class LeadNurturingSchema(BaseModel):
    nurturing_id: Optional[int] = Field(default=None, alias='id')
    lead_id: int
    communication_tools: List[str]
    follow_up_actions: List[str]
    engagement_metrics: dict

    class Config:
        from_attributes = True
        populate_by_name = True
