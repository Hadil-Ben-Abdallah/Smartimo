from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from core.schemas import ResourceSchema

class SustainabilityInitiativeSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    description: str
    implementation_date: str
    resource_savings: Dict[str, float]
    environmental_impact: Dict[str, float]

    class Config:
        from_attributes = True
        populate_by_name = True

class SustainabilityDashboardSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    user_id: int
    energy_consumption: Dict[str, float]
    water_usage: Dict[str, float]
    waste_generation: Dict[str, float]
    ghg_emissions: Dict[str, float]

    class Config:
        from_attributes = True
        populate_by_name = True

class SustainabilityCertificationSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    certification_type: str
    status: str
    submission_deadline: str
    documentation: Dict[str, str]

    class Config:
        from_attributes = True
        populate_by_name = True

class TenantSustainabilityResourceSchema(ResourceSchema):
    tenant_id: int
    category: str

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertySustainabilityRatingSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    rating_type: str
    score: float
    issued_by: str
    issued_date: str

    class Config:
        from_attributes = True
        populate_by_name = True

class SustainabilityForumSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    topic: str
    message: str
    participants_id: int

    class Config:
        from_attributes = True
        populate_by_name = True
