from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class RealEstateAgentSchema(BaseModel):
    properties: List[int] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class ThePropertyListingSchema(BaseModel):
    agent_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertyOwnerSchema(BaseModel):
    properties: List[int] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class ProspectiveBuyerRenterSchema(BaseModel):
    preferences: Dict
    saved_listings: List[int] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class SavedListingSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    user_id: int
    property_id: int
    created_at: str

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertyNotificationSchema(BaseModel):
    user_id: int
    message: str

    class Config:
        from_attributes = True
        populate_by_name = True

