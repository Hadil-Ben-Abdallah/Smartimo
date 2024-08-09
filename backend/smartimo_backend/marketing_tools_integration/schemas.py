from pydantic import BaseModel, Field
from typing import List, Optional
from core.schemas import PropertySchema

class MarketingPropertySchema(PropertySchema):
    virtual_tours: Optional[List[str]]
    media_optimization_recommendations: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True

class ListingDistributionSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    channel: str
    target_audience: str
    category: str
    views: int
    inquiries: int
    engagement_metrics: Optional[dict]

    class Config:
        from_attributes = True
        populate_by_name = True

class SocialMediaPostSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    platform: str
    content: str
    scheduled_time: str
    engagement_metrics: Optional[dict]

    class Config:
        from_attributes = True
        populate_by_name = True

class AdvertisingCampaignSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    platform: str
    target_audience: str
    budget: float
    bidding_strategy: str
    impressions: int
    clicks: int
    conversions: int
    cpa: float

    class Config:
        from_attributes = True
        populate_by_name = True

class MarketingAnalyticsSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    campaign_id: int
    impressions: int
    clicks: int
    conversions: int
    cpl: float
    roi: float
    custom_reports: Optional[dict]

    class Config:
        from_attributes = True
        populate_by_name = True
