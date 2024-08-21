from pydantic import BaseModel, Field
from typing import List, Optional
from core.schemas import UserSchema, PropertySchema

class DemandForecastSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    user_id: int
    historical_data_sources: List[str]
    market_trends: List[str]
    demand_patterns: List[str]
    pricing_trends: List[str]
    forecast_results: List[str]
    scenario_analyses: List[str]

    class Config:
        from_attributes = True
        populate_by_name = True

class MarketDemandSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    user_id: int
    transaction_data: List[str]
    listing_inventory: List[str]
    market_indicators: List[str]
    demand_forecast: List[str]
    visualization_tools: List[str]

    class Config:
        from_attributes = True
        populate_by_name = True

class DevelopmentFeasibilitySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    project_id: int
    user_id: int
    market_research: List[str]
    economic_models: List[str]
    demand_drivers: List[str]
    consumer_preferences: List[str]
    feasibility_results: List[str]
    sensitivity_analysis: List[str]

    class Config:
        from_attributes = True
        populate_by_name = True

class CommercialDemandSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    user_id: int
    leasing_data: List[str]
    market_trends: List[str]
    demand_forecast: List[str]
    tenant_profiles: List[str]
    lease_optimization: List[str]

    class Config:
        from_attributes = True
        populate_by_name = True

class ClientForecastingServiceSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    client_id: int
    demand_forecasting_models: List[str]
    pricing_algorithms: List[str]
    report_templates: List[str]
    client_dashboard: List[str]

    class Config:
        from_attributes = True
        populate_by_name = True

