from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, date

class PropertyDocumentSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    document_type: str
    file_path: str
    property_id: int
    uploaded_by: int
    uploaded_at: datetime
    access_permissions: Dict
    expiration_date: Optional[date]

    class Config:
        from_attributes = True
        populate_by_name = True

class DocumentCategorySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str
    description: Optional[str]
    property_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class DocumentTagSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str
    document_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class DocumentExpirationReminderSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    document_id: int
    reminder_date: date
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class DocumentSharingSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    document_id: int
    shared_with: int
    shared_at: datetime
    access_permissions: Dict
    activity_log: List[Dict]

    class Config:
        from_attributes = True
        populate_by_name = True

class ESignatureIntegrationSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    document_id: int
    signature_status: str
    signed_at: Optional[datetime]
    signing_party: int
    signature_log: List[Dict]

    class Config:
        from_attributes = True
        populate_by_name = True

