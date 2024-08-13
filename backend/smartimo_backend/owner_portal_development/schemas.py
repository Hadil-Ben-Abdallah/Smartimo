from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from pydantic import HttpUrl
from typing import List
from core.schemas import PortalSchema, FinancialReportSchema, NotificationSchema, CommunicationSchema, ResourceSchema

class OwnerPortalSchema(PortalSchema):
    owner: int

class OwnerFinancialReportSchema(FinancialReportSchema):
    owner: int
    property: int
    report_type: str
    document_url: HttpUrl
    
    class Config:
        from_attributes = True
        populate_by_name = True

class PerformanceMetricSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    owner: int
    property: int
    metric_name: str
    occupancy_rate: float
    rental_income: float
    value: float
    date: date

    class Config:
        from_attributes = True
        populate_by_name = True

class OwnerNotificationSchema(NotificationSchema):
    owner: int
    notification_type: str
    delivery_method: str
    frequency: str

    class Config:
        from_attributes = True
        populate_by_name = True

class PortalCommunicationSchema(CommunicationSchema):
    owner: int
    manager: int
    attachments: List[str]
    communication_log: str

    class Config:
        from_attributes = True
        populate_by_name = True

class OwnerResourceSchema(ResourceSchema):
    owner: int

    class Config:
        from_attributes = True
        populate_by_name = True
