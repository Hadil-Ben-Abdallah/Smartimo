from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime
from core.schemas import PropertySchema, NotificationSchema, FeedbackSchema

class VisitorPropertySchema(PropertySchema):
    owner_id: int
    listing_type: str

    class Config:
        from_attributes = True
        populate_by_name = True

class VisitorSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str
    email: str
    phone: str
    visit_purpose: str

    class Config:
        from_attributes = True
        populate_by_name = True

class ShowingSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    agent_id: int
    visitor_id: int
    date: date
    time: time
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class AccessControlSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    visitor_id: int
    access_code: str
    access_start: datetime
    access_end: datetime
    permissions: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class VisitorFeedbackSchema(FeedbackSchema):
    visitor_id: int
    property_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class VisitorNotificationSchema(NotificationSchema):
    visitor_id: int
    type: str
    status: str
    
    class Config:
        from_attributes = True
        populate_by_name = True
