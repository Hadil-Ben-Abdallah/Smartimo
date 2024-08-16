from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from core.schemas import DocumentSchema, NotificationSchema

class SigningDocumentSchema(DocumentSchema):
    signer_list: List[str]
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class SignerSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str
    email: str
    signature: Optional[str] = None
    document_id: int
    signed_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class SigningNotificationSchema(NotificationSchema):
    signer_id: int
    document_id: int
    type: str
    delivery_method: str

    class Config:
        from_attributes = True
        populate_by_name = True

class ComplianceSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    document_id: int
    regulation: str
    compliance_status: str
    last_checked: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class SignatureTrackerSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    document_id: int
    signer_id: int
    status: str
    reminder_sent: bool

    class Config:
        from_attributes = True
        populate_by_name = True
