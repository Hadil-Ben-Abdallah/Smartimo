from ninja import Router
from typing import List
from .models import VisitorProperty, Visitor, AccessControl, VisitorFeedback, VisitorNotification
from .schemas import ShowingSchema, VisitorSchema, AccessControlSchema, VisitorFeedbackSchema, VisitorNotificationSchema

router = Router()

@router.post("/schedule_showing", response=ShowingSchema)
def schedule_showing(request, payload: ShowingSchema):
    showing = VisitorProperty.objects.get(id=payload.property_id).schedule_showing(payload.dict(exclude={'id'}))
    showing.send_invitation()
    return showing

@router.get("/get_showings/{property_id}", response=List[ShowingSchema])
def get_showings(request, property_id: int):
    showings = VisitorProperty.objects.get(id=property_id).get_showings()
    return list(showings)

@router.post("/add_visitor", response=VisitorSchema)
def add_visitor(request, payload: VisitorSchema):
    visitor = Visitor.objects.create(**payload.dict(exclude={'id'}))
    return visitor

@router.post("/grant_access", response=AccessControlSchema)
def grant_access(request, payload: AccessControlSchema):
    access = AccessControl.objects.create(**payload.dict(exclude={'id'}))
    return access

@router.post("/submit_feedback", response=VisitorFeedbackSchema)
def submit_feedback(request, payload: VisitorFeedbackSchema):
    feedback = VisitorFeedback.objects.create(**payload.dict(exclude={'id'}))
    return feedback

@router.get("/get_notifications/{visitor_id}", response=List[VisitorNotificationSchema])
def get_notifications(request, visitor_id: int):
    notifications = VisitorNotification.objects.filter(visitor_id=visitor_id)
    return list(notifications)

