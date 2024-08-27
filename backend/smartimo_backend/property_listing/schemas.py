from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import List, Dict, Optional
from datetime import datetime, date
from core.schemas import UserSchema, PropertySchema, NotificationSchema

class AgencySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str
    bank_partnership: str
    founding_date: date
    bank_code: str
    description: str
    email: EmailStr
    website_link: HttpUrl
    phone_number: str
    location: str

    class Config:
        from_attributes = True
        populate_by_name = True

class RealEstateAgentSchema(UserSchema):
    agency: int

    class Config:
        from_attributes = True
        populate_by_name = True

class ThePropertyListingSchema(PropertySchema):
    agent_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertyOwnerSchema(UserSchema):
    properties: List[int] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class ProspectiveBuyerRenterSchema(UserSchema):
    preferences: Dict
    saved_listings: List[int] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class SavedListingSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    user_id: int
    property_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertyNotificationSchema(NotificationSchema):
    user_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

