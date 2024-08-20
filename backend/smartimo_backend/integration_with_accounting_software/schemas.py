from ninja import Schema
from typing import Optional
from pydantic import Field
from datetime import datetime, date
from lease_rental_management.schemas import PropertyManagerSchema
from core.schemas import ReportSchema

class IntegrationPropertyManagerSchema(PropertyManagerSchema):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class IntegrationSettingsSchema(Schema):
    id: Optional[int] = Field(default=None, alias='id')
    property_manager_id: int
    accounting_software: str
    sync_frequency: str
    data_mapping_rules: dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class IntegrationFinancialReportSchema(ReportSchema):
    report_type: str
    property_id: int
    generated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class ReconciliationSchema(Schema):
    id: Optional[int] = Field(default=None, alias='id')
    property_manager_id: int
    bank_transactions: dict
    ledger_entries: dict
    reconciliation_date: date
    discrepancies: dict
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class ExportSchema(Schema):
    id: Optional[int] = Field(default=None, alias='id')
    property_manager_id: int
    export_type: str
    export_format: str
    date_range: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True
