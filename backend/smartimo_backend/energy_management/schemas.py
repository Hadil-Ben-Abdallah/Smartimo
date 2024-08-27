from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class EnergyMonitoringDeviceSchema(BaseModel):
    id: int
    property_id: int
    device_type: str
    installation_date: date
    last_maintenance_date: date

    class Config:
        from_attributes = True
        populate_by_name = True

class EnergyDashboardSchema(BaseModel):
    id: int
    user_id: int
    energy_consumption: float
    cost_metrics: float
    historical_trends: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class EnergyGoalSchema(BaseModel):
    id: int
    property_id: int
    target_value: float
    benchmark: str
    current_value: float
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class EnergyRecommendationSchema(BaseModel):
    id: int
    tenant_id: int
    recommendation_text: str
    category: str

    class Config:
        from_attributes = True
        populate_by_name = True

class EnergyModelingToolSchema(BaseModel):
    id: int
    developer_id: int
    building_design: dict
    energy_performance: float
    roi_projections: float

    class Config:
        from_attributes = True
        populate_by_name = True

class EnergyAuditSchema(BaseModel):
    id: int
    property_id: int
    audit_date: date
    audit_results: dict
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class EnergyProjectSchema(BaseModel):
    id: int
    manager_id: int
    project_type: str
    start_date: date
    end_date: date
    status: str
    impact_metrics: dict

    class Config:
        from_attributes = True
        populate_by_name = True
