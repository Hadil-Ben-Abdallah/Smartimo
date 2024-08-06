from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class LeaseRentalAgreementSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    tenant_id: int
    # manager_id: int
    terms: dict
    rent_amount: float
    security_deposit: float
    signed_document: Optional[str]
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class CreateLeaseRentalAgreementSchema(BaseModel):
    property_id: int
    tenant_id: int
    terms: dict
    rent_amount: float
    security_deposit: float
    signed_document: Optional[str] = None
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class UpdateLeaseRentalAgreementSchema(BaseModel):
    terms: Optional[dict] = None
    rent_amount: Optional[dict] = None
    signed_document: Optional[str] = None
    start_date: Optional[dict] = None
    end_date: Optional[dict] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class LeaseRentalTenantSchema(BaseModel):
    name: str
    email: str
    phone: str
    lease_agreements: List[LeaseRentalAgreementSchema]
    payment_history: List[dict]

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertyManagerSchema(BaseModel):
    # id: Optional[int] = Field(default=None, alias='id')
    properties: List[int]
    lease_agreements: List[LeaseRentalAgreementSchema]

    class Config:
        from_attributes = True
        populate_by_name = True

class RentalPaymentSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    lease_agreement_id: int
    tenant_id: int
    amount: float
    payment_date: datetime
    payment_method: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CreateRentalPaymentSchema(BaseModel):
    lease_agreement_id: int
    tenant_id: int
    amount: float
    payment_date: datetime
    payment_method: str

    class Config:
        from_attributes = True
        populate_by_name = True

class LeaseRentalCommunicationSchema(BaseModel):
    tenant_id: int
    manager_id: int
    type: str
    message: str
    response: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True





# from ninja import Schema
# from pydantic import BaseModel, Field
# from datetime import datetime
# from typing import List, Optional

# class PropertyManager (BaseModel):
#     id: Optional[int] = Field(default=None, alias='id')
#     name: str
#     email: str

# class LeaseRentalAgreementSchema(BaseModel):
#     property_id: int
#     manager_id: int
#     terms: dict
#     signed_document: Optional[str]
#     created_at: datetime
#     updated_at: datetime

# class CreateLeaseRentalAgreementSchema(BaseModel):
#     property_id: int
#     manager_id: int
#     terms: dict
#     signed_document: Optional[str] = None

# class UpdateLeaseRentalAgreementSchema(BaseModel):
#     terms: Optional[dict] = None
#     signed_document: Optional[str] = None

# class LeaseRentalTenantSchema(BaseModel):
#     name: str
#     email: str
#     phone: str
#     lease_agreements: List[LeaseRentalAgreementSchema]
#     payment_history: List[dict]

# class PropertyManagerSchema(BaseModel):
#     name: str
#     email: str
#     phone: str
#     properties: List[int]
#     lease_agreements: List[LeaseRentalAgreementSchema]

# class RentalPaymentSchema(Schema):
#     id: Optional[int] = Field(default=None, alias='id')
#     lease_agreement_id: int
#     tenant_id: int
#     amount: float
#     payment_date: datetime
#     payment_method: str
#     status: str

# class CreateRentalPaymentSchema(BaseModel):
#     lease_agreement_id: int
#     tenant_id: int
#     amount: float
#     payment_date: datetime
#     payment_method: str

# class LeaseRentalCommunicationSchema(BaseModel):
#     id: int
#     tenant_id: int
#     manager_id: int
#     type: str
#     message: str
#     response: Optional[str]
