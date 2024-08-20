from typing import  Dict
from core.schemas import ReportSchema


class CustomizableFinancialReportSchema(ReportSchema):
    property_owner_id: int
    filters: str
    groupings: Dict
    sort_options: Dict

    class Config:
        from_attributes = True
        populate_by_name = True


class SalesReportSchema(ReportSchema):
    real_estate_agent_id: int
    template: str
    fields: str
    filters: str
    visualizations: Dict

    class Config:
        from_attributes = True
        populate_by_name = True


class MaintenanceReportSchema(ReportSchema):
    property_manager_id: int
    fields: str
    filters: str
    dashboard: Dict

    class Config:
        from_attributes = True
        populate_by_name = True


class InvestmentReportSchema(ReportSchema):
    fields: str
    filters: str
    external_data_sources: Dict

    class Config:
        from_attributes = True
        populate_by_name = True


class ComplianceReportSchema(ReportSchema):
    template: str
    fields: str
    filters:str

    class Config:
        from_attributes = True
        populate_by_name = True
