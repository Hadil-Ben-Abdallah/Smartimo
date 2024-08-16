from pydantic import BaseModel
from typing import List, Optional
from pydantic import Field
from datetime import datetime

class RegulationRepositorySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    title: str
    content: str
    location: str
    property_type: str
    compliance_category: str
    version: str
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class LegalDocumentGeneratorSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    template_name: str
    template_content: str
    property_details: dict
    transaction_details: dict
    signatures: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class ComplianceCalendarSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    event_id: int
    reminders: Optional[List[str]]
    compliance_task: str

    class Config:
        from_attributes = True
        populate_by_name = True

class DueDiligenceCheckerSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    check_type: str
    results: str
    risk_assessment: str

    class Config:
        from_attributes = True
        populate_by_name = True

class FairHousingComplianceSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    training_module: str
    checklist: dict
    audit_trail: dict

    class Config:
        from_attributes = True
        populate_by_name = True
