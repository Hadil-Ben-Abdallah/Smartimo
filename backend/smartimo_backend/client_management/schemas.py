from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from core.schemas import UserSchema, ClientInteractionSchema, ReminderSchema
from property_listing.schemas import RealEstateAgentSchema

class ClientSchema(UserSchema):
    preferences: Dict
    tags: List[str]
    client_status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    agent_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class InteractionSchema(ClientInteractionSchema):
    client_id: int
    agent_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class ClientReminderSchema(ReminderSchema):
    client_id: int
    agent_id: int
    task: str

    class Config:
        from_attributes = True
        populate_by_name = True

class ClientAnalyticsSchema(BaseModel):
    client_id: int
    engagement_metrics: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

class ClientRealEstateAgentSchema(RealEstateAgentSchema):
    clients: List[ClientSchema]

    class Config:
        from_attributes = True
        populate_by_name = True
