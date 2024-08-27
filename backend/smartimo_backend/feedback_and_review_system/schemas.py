from pydantic import BaseModel, Field
from typing import Optional
from core.schemas import FeedbackSchema, NotificationSchema

class UserFeedbackSchema(FeedbackSchema):
    user: int
    property: int

    class Config:
        from_attributes = True
        populate_by_name = True

class SurveySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    title: str
    description: str
    questions: dict

    class Config:
        from_attributes = True
        populate_by_name = True

class ReviewSchema(FeedbackSchema):
    user: int
    property: int

    class Config:
        from_attributes = True
        populate_by_name = True

class FeedbackNotificationSchema(NotificationSchema):
    user: int
    feedback: int
    type: str
    channel: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True

class AnalyticsSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    feedback_data: dict
    survey_data: dict
    review_data: dict

    class Config:
        from_attributes = True
        populate_by_name = True
