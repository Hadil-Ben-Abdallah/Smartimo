from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from .models import Appointment, Inspection, Task, TaskManager, Event, CalendarIntegration
from .schemas import (
    AppointmentSchema,
    InspectionSchema,
    TaskSchema,
    TaskManagerSchema,
    EventSchema,
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

# TaskManager Endpoints
@router.post("/taskmanager/", response=TaskManagerSchema)
def create_task_manager(request, payload: TaskManagerSchema):
    task_manager = TaskManager.objects.create(**payload.dict(exclude={'id'}))
    return task_manager

@router.get("/taskmanager/{task_id}", response=TaskManagerSchema)
def get_task_manager(request, task_id: int):
    task_manager = TaskManager.objects.get(id=task_id)
    return task_manager

# Event Endpoints
@router.get("/events/", response=List[EventSchema])
def list_event(request):
    return Event.objects.all()

@router.post("/events/", response=EventSchema)
def create_event(request, payload: EventSchema):
    payload_dict = payload.dict(exclude_unset=True, exclude={'id'})
    event = Event.objects.create(**payload_dict)
    return event

@router.get("/events/{event_id}/", response=EventSchema)
def get_event(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    return event

@router.put("/events/{event_id}/", response=EventSchema)
def update_event(request, event_id: int, payload: EventSchema):
    event = get_object_or_404(Event, id=event_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(event, attr, value)
    event.save()
    return event

@router.delete("/events/{event_id}/", response=None)
def delete_event(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
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

