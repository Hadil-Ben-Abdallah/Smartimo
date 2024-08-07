from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import date, datetime
from core.schemas import FinancialReportSchema

class InvoiceSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    tenant_id: int
    property_id: int
    amount_due: float
    due_date: date
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    itemized_charges: Any
    payment_instructions: str

    class Config:
        from_attributes = True
        populate_by_name = True

class PaymentSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    invoice_id: int
    user_id: int
    credit_card_number: str
    reached_amount: float
    remaining_amount: float
    payment_date: date
    payment_method: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class TheFinancialReportSchema(FinancialReportSchema):
    property_id: int
    report_type: str
    report_period: str

    class Config:
        from_attributes = True
        populate_by_name = True

class FinancialTransactionSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    transaction_date: date
    amount: float
    transaction_type: str
    description: str

    class Config:
        from_attributes = True
        populate_by_name = True

class TenantPortalSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    tenant_id: int
    invoices: List[InvoiceSchema]
    payment_history: List[PaymentSchema]

    class Config:
        from_attributes = True
        populate_by_name = True
