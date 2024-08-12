from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime, date

class PropertySchema(BaseModel):
    property_id: Optional[int] = Field(default=None, alias='property_id')
    type: str
    description: str
    address: str
    photos: str
    videos: str
    size: float
    bathroom_number: int
    badroom_number: int
    garage: bool
    garden: bool
    swiming_pool: bool
    year_built: datetime 
    price: float
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
        populate_by_name = True

class NotificationSchema(BaseModel):
    notification_id: Optional[int] = Field(default=None, alias='notification_id')
    message: str
    status: str
    date: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class ReminderSchema(BaseModel):
    reminder_id: Optional[int] = Field(default=None, alias='reminder_id')
    message_content: str
    reminder_date: datetime
    frequency: str
    delivary_channel: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class ClientInteractionSchema(BaseModel):
    client_interaction_id: Optional[int] = Field(default=None, alias='client_interaction_id')
    interaction_type: str
    notes: str

    class Config:
        from_attributes = True
        populate_by_name = True

# class LeaseAgreementSchema(BaseModel):

#     lease_id: Optional[int] = Field(default=None, alias='lease_id')
#     tenant_id: int
#     start_date: str
#     end_date: str
#     rent_amount: float
#     security_deposit: float

#     class Config:
#         from_attributes = True
#         populate_by_name = True

class CommunicationSchema(BaseModel):
    communication_id: Optional[int] = Field(default=None, alias='communication_id')
    message: str
    date: str

    class Config:
        from_attributes = True
        populate_by_name = True

# class PropertyListingSchema(BaseModel):
#     property_listing_id: Optional[int] = Field(default=None, alias='property_listing_id')
#     type: str
#     description: str
#     address: str
#     photo: str
#     video: str
#     size: float
#     bathroom_number: int
#     badroom_number: int
#     garage: bool
#     garden: bool
#     swiming_pool: bool
#     year_built: datetime 
#     price: float
#     status: str

#     class Config:
#         from_attributes = True
#         populate_by_name = True

class FinancialReportSchema(BaseModel):
    financial_report_id: Optional[int] = Field(default=None, alias='financial_report_id')
    financial_data: Dict
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
        populate_by_name = True

class SalesOpportunitySchema(BaseModel):
    sales_opportunity_id: Optional[int] = Field(default=None, alias='sales_opportunity_id')
    value: float
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class ResourceSchema(BaseModel):
    resource_id: Optional[int] = Field(default=None, alias='resource_id')
    title: str
    content: str
    contact_info: str

    class Config:
        from_attributes = True
        populate_by_name = True

class UserSchema(BaseModel):
    user_id: Optional[int] = Field(default=None, alias='user_id')
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    cin: str
    birth_date: str
    phone: str
    address: str
    credit_card_number: str
    job_title: str
    user_type: str

    class Config:
        from_attributes = True
        populate_by_name = True

class DocumentSchema(BaseModel):
    document_id: Optional[int] = Field(default=None, alias='document_id')
    title: str
    document_type: str
    file_path: str
    description: str
    uploaded_by: int
    uploaded_at: datetime
    version: str
    access_permissions: Dict
    expiration_date: date

    class Config:
        from_attributes = True
        populate_by_name = True

class PortalSchema(BaseModel):
    portal_id: Optional[int] = Field(default=None, alias='portal_id')
    name:str
    version:str
    url:str

    class Config:
        from_attributes = True
        populate_by_name = True

# class VendorSchema(BaseModel):
#     vendor_id: Optional[int] = Field(default=None, alias='vendor_id')
#     name: str
#     certifications: str

#     class Config:
#         from_attributes = True
#         populate_by_name = True
