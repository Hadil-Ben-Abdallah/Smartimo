from pydantic import BaseModel, Field
from typing import List, Optional
from core.schemas import ResourceSchema
from task_calendar_management.schemas import EventSchema

class CommunitySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str
    description: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class ForumSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    community_id: int
    name: str
    description: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class ThreadSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    forum_id: int
    title: str
    content: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class ReplySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    thread_id: int
    content: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class AnnouncementSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    community_id: int
    title: str
    content: str
    category: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    archived: bool

    class Config:
        from_attributes = True
        populate_by_name = True

class SubscriberSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    announcement_id: int
    user_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class CommunityEventSchema(EventSchema):
    community_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class RSVP_Schema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    event_id: int
    user_id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class CommunityResourceSchema(ResourceSchema):
    community_id: int
    category: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class ReviewSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    resource_id: int
    details: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class PollSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    community_id: int
    question: str
    options: List[str]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class PollVoteSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    poll_id: int
    option: int
    user_id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
