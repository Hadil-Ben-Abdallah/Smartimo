from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from core.schemas import ReportSchema

class AnalyticsReportSchema(ReportSchema):
    type: str
    created_by: str
    filters: Dict
    visualizations: List[Dict]

    class Config:
        from_attributes = True
        populate_by_name = True

class PropertyPerformanceReportSchema(AnalyticsReportSchema):
    occupancy_rate: float
    average_rental_income: float
    vacancy_rate: float
    maintenance_costs: float
    noi: float

class SalesTrendReportSchema(AnalyticsReportSchema):
    sales_volume: float
    average_selling_price: float
    time_on_market: float
    regional_sales_distribution: Dict

class FinancialPerformanceReportSchema(AnalyticsReportSchema):
    rental_income: float
    operating_expenses: float
    cash_flow: float
    roi: float

class ClientEngagementReportSchema(AnalyticsReportSchema):
    lead_conversion_rate: float
    inquiry_response_time: float
    client_satisfaction_score: float

class AutomatedReportSchedulerSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    report: AnalyticsReportSchema
    frequency: str
    recipients: List[str]
    delivery_channel: str
    last_run: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True
