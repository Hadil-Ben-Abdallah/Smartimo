from ninja import Router
from .models import Community, Forum, Announcement, CommunityEvent, CommunityResource, Poll
from .schemas import (
    CommunitySchema, ForumSchema, AnnouncementSchema, CommunityEventSchema,
    CommunityResourceSchema, PollSchema
)

router = Router()

@router.post("/communities/", response=CommunitySchema)
def create_community(request, data: CommunitySchema):
    community = Community.objects.create(**data.dict(exclude={'id'}))
    return community

@router.get("/communities/{community_id}", response=CommunitySchema)
def get_community(request, community_id: int):
    return Community.objects.get(id=community_id)

@router.put("/communities/{community_id}", response=CommunitySchema)
def update_community(request, community_id: int, data: CommunitySchema):
    community = Community.objects.get(id=community_id)
    payload = data.dict(exclude_unset=True)
    for key, value in payload.items():
        if key != 'id':
            setattr(community, key, value)
    community.save()
    return community

@router.delete("/communities/{community_id}")
def delete_community(request, community_id: int):
    community = Community.objects.get(id=community_id)
    community.delete()
    return {"success": True}

@router.post("/forums/", response=ForumSchema)
def create_forum(request, data: ForumSchema):
    return Forum.objects.create(**data.dict(exclude={'id'}))

@router.post("/announcements/", response=AnnouncementSchema)
def post_announcement(request, data: AnnouncementSchema):
    return Announcement.objects.create(**data.dict(exclude={'id'}))

@router.post("/events/", response=CommunityEventSchema)
def schedule_event(request, data: CommunityEventSchema):
    return CommunityEvent.objects.create(**data.dict(exclude={'id'}))

@router.post("/resources/", response=CommunityResourceSchema)
def add_resource(request, data: CommunityResourceSchema):
    return CommunityResource.objects.create(**data.dict(exclude={'id'}))

@router.post("/polls/", response=PollSchema)
def create_poll(request, data: PollSchema):
    return Poll.objects.create(**data.dict(exclude={'id'}))

@router.put("/polls/{poll_id}", response=PollSchema)
def update_poll(request, poll_id: int, data: PollSchema):
    poll = Poll.objects.get(id=poll_id)
    payload = data.dict(exclude_unset=True)
    for key, value in payload.items():
        if key != 'id':
            setattr(poll, key, value)
    poll.save()
    return poll

