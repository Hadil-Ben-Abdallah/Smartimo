from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from core.schemas import UserSchema, PropertySchema, CommunicationSchema, NotificationSchema

class MobileAppSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    app_name: str
    version: str
    platform: str
    store_url: str

    class Config:
        from_attributes = True
        populate_by_name = True

class AppPropertySchema(PropertySchema):
    features: List[str]
    saved: bool

    class Config:
        from_attributes = True
        populate_by_name = True

class CommunicationManagerSchema(CommunicationSchema):
    id: int
    messages: List[Dict]
    notifications: List[Dict]
    inbox: List[Dict]

    class Config:
        from_attributes = True
        populate_by_name = True

class NotificationManagerSchema(NotificationSchema):
    user_preferences: Dict

    class Config:
        from_attributes = True
        populate_by_name = True

class MobileUserAccountSchema(UserSchema):
    ssologin: bool

    class Config:
        from_attributes = True
        populate_by_name = True
