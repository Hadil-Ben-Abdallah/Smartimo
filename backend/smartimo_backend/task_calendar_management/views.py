from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from .models import Appointment, Inspection, Task, Meeting, CalendarIntegration
from .schemas import (
    AppointmentSchema,
    InspectionSchema,
    TaskSchema,
    MeetingSchema,
    CalendarIntegrationSchema
)

router = Router()

# Appointment Endpoints
@router.get("/appointments/", response=List[AppointmentSchema])
def list_appointments(request):
    return Appointment.objects.all()

@router.post("/appointments/", response=AppointmentSchema)
def create_appointment(request, payload: AppointmentSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    appointment = Appointment.objects.create(**payload_dict)
    return appointment

@router.get("/appointments/{appointment_id}/", response=AppointmentSchema)
def get_appointment(request, appointment_id: int):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return appointment

@router.put("/appointments/{appointment_id}/", response=AppointmentSchema)
def update_appointment(request, appointment_id: int, payload: AppointmentSchema):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(appointment, attr, value)
    appointment.save()
    return appointment

@router.delete("/appointments/{appointment_id}/", response=None)
def delete_appointment(request, appointment_id: int):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return None

# Inspection Endpoints
@router.get("/inspections/", response=List[InspectionSchema])
def list_inspections(request):
    return Inspection.objects.all()

@router.post("/inspections/", response=InspectionSchema)
def create_inspection(request, payload: InspectionSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    inspection = Inspection.objects.create(**payload_dict)
    return inspection

@router.get("/inspections/{inspection_id}/", response=InspectionSchema)
def get_inspection(request, inspection_id: int):
    inspection = get_object_or_404(Inspection, id=inspection_id)
    return inspection

@router.put("/inspections/{inspection_id}/", response=InspectionSchema)
def update_inspection(request, inspection_id: int, payload: InspectionSchema):
    inspection = get_object_or_404(Inspection, id=inspection_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(inspection, attr, value)
    inspection.save()
    return inspection

@router.delete("/inspections/{inspection_id}/", response=None)
def delete_inspection(request, inspection_id: int):
    inspection = get_object_or_404(Inspection, id=inspection_id)
    inspection.delete()
    return None

# Task Endpoints
@router.get("/tasks/", response=List[TaskSchema])
def list_tasks(request):
    return Task.objects.all()

@router.post("/tasks/", response=TaskSchema)
def create_task(request, payload: TaskSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    task = Task.objects.create(**payload_dict)
    return task

@router.get("/tasks/{task_id}/", response=TaskSchema)
def get_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    return task

@router.put("/tasks/{task_id}/", response=TaskSchema)
def update_task(request, task_id: int, payload: TaskSchema):
    task = get_object_or_404(Task, id=task_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(task, attr, value)
    task.save()
    return task

@router.delete("/tasks/{task_id}/", response=None)
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return None

# Meeting Endpoints
@router.get("/meetings/", response=List[MeetingSchema])
def list_meetings(request):
    return Meeting.objects.all()

@router.post("/meetings/", response=MeetingSchema)
def create_meeting(request, payload: MeetingSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    meeting = Meeting.objects.create(**payload_dict)
    return meeting

@router.get("/meetings/{meeting_id}/", response=MeetingSchema)
def get_meeting(request, meeting_id: int):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    return meeting

@router.put("/meetings/{meeting_id}/", response=MeetingSchema)
def update_meeting(request, meeting_id: int, payload: MeetingSchema):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(meeting, attr, value)
    meeting.save()
    return meeting

@router.delete("/meetings/{meeting_id}/", response=None)
def delete_meeting(request, meeting_id: int):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.delete()
    return None

# Calendar Integration Endpoints
@router.get("/calendar-integrations/", response=List[CalendarIntegrationSchema])
def list_calendar_integrations(request):
    return CalendarIntegration.objects.all()

@router.post("/calendar-integrations/", response=CalendarIntegrationSchema)
def create_calendar_integration(request, payload: CalendarIntegrationSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'user_id'})
    integration = CalendarIntegration.objects.create(**payload_dict)
    return integration

@router.get("/calendar-integrations/{integration_id}/", response=CalendarIntegrationSchema)
def get_calendar_integration(request, integration_id: int):
    integration = get_object_or_404(CalendarIntegration, id=integration_id)
    return integration

@router.put("/calendar-integrations/{integration_id}/", response=CalendarIntegrationSchema)
def update_calendar_integration(request, integration_id: int, payload: CalendarIntegrationSchema):
    integration = get_object_or_404(CalendarIntegration, id=integration_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(integration, attr, value)
    integration.save()
    return integration

@router.delete("/calendar-integrations/{integration_id}/", response=None)
def delete_calendar_integration(request, integration_id: int):
    integration = get_object_or_404(CalendarIntegration, id=integration_id)
    integration.delete()
    return None

