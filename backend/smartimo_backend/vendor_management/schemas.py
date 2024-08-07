from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from lease_rental_management.schemas import PropertyManagerSchema, CommunicationSchema

class VendorSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    certifications: List[str]
    service_specialties: List[str]
    insurance_details: Optional[str]
    rating: float
    reviews: List[str]
    documents: List[str]
    pricing_model: str
    service_areas: List[str]
    availability: dict
    profile_content: dict

    class Config:
        from_attributes = True
        populate_by_name = True


class VendorsPropertyManagerSchema(PropertyManagerSchema):
    managed_vendors: List[int]

    class Config:
        from_attributes = True
        populate_by_name = True


class ContractSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    vendor_id: int
    property_manager_id: int
    scope_of_work: str
    pricing: float
    payment_terms: str
    sla: str
    document_version: int
    expiry_date: date
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True


class PerformanceMetricsSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    vendor_id: int
    response_time: float
    resolution_time: float
    customer_satisfaction_score: float
    compliance_sla: float
    feedback: List[str]

    class Config:
        from_attributes = True
        populate_by_name = True


class VendorsCommunicationSchema(CommunicationSchema):
    sender_id: int
    receiver_id: int
    status: str
    message: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True
