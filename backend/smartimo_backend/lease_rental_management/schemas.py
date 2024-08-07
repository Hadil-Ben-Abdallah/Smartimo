from ninja import Schema
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from core.schemas import CommunicationSchema

class AgreementSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    tenant_id: int
    terms: dict
    rent_amount: float
    security_deposit: float
    signed_document: Optional[str]
    start_date: date
    end_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class TenantSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    username: str
    lease_agreements: List[AgreementSchema]
    payment_history: list

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertyManagerSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    username: str
    properties: List[int]
    lease_agreements: List[AgreementSchema]

    class Config:
        from_attributes = True
        populate_by_name = True

class RentalPaymentSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    lease_agreement_id: int
    tenant_id: int
    amount: float
    payment_date: date
    payment_method: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class LeaseRentalCommunicationSchema(CommunicationSchema):
    tenant_id: int
    manager_id: int
    type: str
    response: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True
