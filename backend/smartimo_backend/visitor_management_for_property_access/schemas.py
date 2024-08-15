from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime
from core.schemas import PropertySchema, NotificationSchema


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
    created_at: datetime
    updated_at: datetime

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
    created_at: datetime
    updated_at: datetime

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
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class FeedbackSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    visitor_id: int
    property_id: int
    rating: int
    comments: str
    created_at: datetime
    updated_at: datetime

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
