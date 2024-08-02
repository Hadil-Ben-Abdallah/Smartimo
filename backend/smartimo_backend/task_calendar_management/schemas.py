from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from pydantic import Field

class AppointmentSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    agent_id: int
    client_id: int
    date: date
    time: str
    type: str
    status: str
    details: str

    class Config:
        from_attributes = True
        populate_by_name = True

class InspectionSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    manager_id: int
    date: date
    time: str
    checklist: dict
    status: str
    report: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class TaskSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    user_id: int
    title: str
    description: str
    priority: str
    deadline: date
    status: str
    category: str

    class Config:
        from_attributes = True
        populate_by_name = True

class MeetingSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    organizer_id: int
    participants: List[int]
    date: date
    time: str
    topic: str
    agenda: str
    location: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CalendarIntegrationSchema(BaseModel):
    user_id: int
    calendar_service: str
    sync_status: str
    last_sync: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True
