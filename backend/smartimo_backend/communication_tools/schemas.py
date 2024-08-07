from pydantic import BaseModel, Field
from typing import List, Optional
from core.schemas import NotificationSchema

class EmailSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    sender_id: int
    recipient_id: int
    subject: str
    body: str
    attachments: List[str] = []
    timestamp: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CommunicationNotificationSchema(NotificationSchema):
    sender_id: int
    recipient_id: int
    message: str
    type: str

    class Config:
        from_attributes = True
        populate_by_name = True

class InstantMessageSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    sender_id: int
    recipient_id: int
    content: str
    attachments: List[str] = []
    timestamp: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class SMSNotificationSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    sender_id: int
    recipient_id: int
    message: str
    timestamp: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CommunicationLogSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    client_id: Optional[int] = None
    property_id: Optional[int] = None
    communication_type: str
    
    class Config:
        from_attributes = True
        populate_by_name = True
