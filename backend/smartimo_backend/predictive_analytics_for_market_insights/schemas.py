from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Optional
from core.schemas import UserSchema

class PredictiveAnalyticsSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    data_source: str
    algorithm: str
    parameters: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

class InvestmentDashboardSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    user_id: int
    predicted_values: Dict
    investment_returns: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

class MarketTrendAnalysisSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    region: str
    property_type: str
    trend_data: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

class RentalDemandForecastSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_manager_id: int
    demand_projections: Dict
    tenant_preferences: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertyValuationModelSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    predicted_value: float
    growth_factors: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

class RealEstaeDeveloperSchema(UserSchema):
    projects: Dict
    market_analysis_id: int
    investment_strategies:Dict
    demand_forecast_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class DevelopmentFeasibilityToolSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    developer_id: int
    project_parameters: Dict
    roi_projections: Dict
    risk_factors: Dict

    class Config:
        from_attributes = True
        populate_by_name = True
