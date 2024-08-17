from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Optional

class PredictiveAnalyticsSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    data_source: str
    algorithm: str
    parameters: Dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class InvestmentDashboardSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    user_id: int
    predicted_values: Dict
    investment_returns: Dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MarketTrendAnalysisSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    region: str
    property_type: str
    trend_data: Dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class RentalDemandForecastSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_manager_id: int
    demand_projections: Dict
    tenant_preferences: Dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PropertyValuationModelSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    predicted_value: float
    growth_factors: Dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DevelopmentFeasibilityToolSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    agent_id: int
    project_parameters: Dict
    roi_projections: Dict
    risk_factors: Dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
