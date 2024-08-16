from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime, date
from core.schemas import PropertySchema, NotificationSchema

class InventoryItemSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    category: str
    name: str
    quantity: int
    description: str
    condition: str
    photos: List[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class InventoryPropertySchema(PropertySchema):
    listing_type: str
    furnished: bool
    inventory_list: List[InventoryItemSchema]

    class Config:
        from_attributes = True
        populate_by_name = True

class MaintenanceLogSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    item_id: int
    activity: str
    service_provider: str
    cost: float
    date: date
    next_maintenance_date: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class DepreciationRecordSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    item_id: int
    initial_value: float
    current_value: float
    depreciation_rate: float
    depreciation_value: float
    last_depreciation_date: date

    class Config:
        from_attributes = True
        populate_by_name = True

class InventoryNotificationSchema(NotificationSchema):
    id: int
    property_manager_id: int
    type: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True
