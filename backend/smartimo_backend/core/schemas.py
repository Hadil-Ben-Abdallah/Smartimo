from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class PropertySchema(BaseModel):
    property_id: Optional[int] = Field(default=None, alias='property_id')
    address: str
    description: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
        populate_by_name = True

class NotificationSchema(BaseModel):
    notification_id: Optional[int] = Field(default=None, alias='notification_id')
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

class PropertyListingSchema(BaseModel):
    property_listing_id: Optional[int] = Field(default=None, alias='property_listing_id')
    type: str
    description: str
    address: str
    photo: str
    video: str
    size: float
    price: float
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

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
    name: str
    email: str
    cin: str
    birth_date: str
    phone: str
    address: str
    user_type: str

    class Config:
        from_attributes = True
        populate_by_name = True

class VendorSchema(BaseModel):
    vendor_id: Optional[int] = Field(default=None, alias='vendor_id')
    name: str
    certifications: str

    class Config:
        from_attributes = True
        populate_by_name = True
