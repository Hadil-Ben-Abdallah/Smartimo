from django.db import models
from core.models import Property, Notification, Feedback, TimeStampedModel
from lease_rental_management.models import Tenant
from task_calendar_management.models import Event
from datetime import timezone

class CalendarEvent(Event):
    tags = models.JSONField(default=list, blank=True, null=True)

    def create_event(self, title, date, time, topic, location, description, organizer, participants, agenda, status, tags):
        self.title = title
        self.date = date
        self.time = time
        self.topic = topic
        self.location = location
        self.description = description
        self.organizer = organizer
        self.participants = participants
        self.agenda = agenda
        self.status = status
        self.tags = tags
        self.save()
        return self

    def edit_event(self, event_id, updates):
        event = CalendarEvent.objects.get(id=event_id)
        for key, value in updates.items():
            setattr(event, key, value)
        event.save()
        return event

    def delete_event(self, event_id):
        event = CalendarEvent.objects.get(id=event_id)
        event.delete()

    def get_event_details(self, event_id):
        return CalendarEvent.objects.get(id=event_id)


class RSVP(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    response = models.CharField(max_length=50, blank=True, null=True)
    responded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def submit_rsvp(self, event_id, tenant_id, response):
        rsvp, created = RSVP.objects.get_or_create(event=event_id, tenant=tenant_id)
        rsvp.response = response
        rsvp.responded_at = timezone.now()
        rsvp.save()
        return rsvp

    def update_rsvp(self, rsvp_id, response):
        rsvp = RSVP.objects.get(id=rsvp_id)
        rsvp.response = response
        rsvp.responded_at = timezone.now()
        rsvp.save()
        return rsvp


class Calendar(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    events = models.ManyToManyField(CalendarEvent, related_name='calendars')
    customization_settings = models.JSONField(default=dict, blank=True, null=True)

    def add_event(self, event):
        self.events.add(event)
        self.save()

    def remove_event(self, event_id):
        event = CalendarEvent.objects.get(id=event_id)
        self.events.remove(event)
        self.save()

    def customize_calendar(self, settings):
        self.customization_settings.update(settings)
        self.save()

    def view_calendar(self, property_id):
        return Calendar.objects.filter(property_id=property_id).first()


class EventNotification(Notification):
    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def schedule_notifications(self, event_id):
        event = CalendarEvent.objects.get(id=event_id)
        tenants = event.agenda.first().tenant.all()
        for tenant in tenants:
            EventNotification.objects.create(event=event, tenant=tenant)
        return True


class EventFeedback(Feedback):
    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)

    def get_event_feedback(self):
        return f"This event {self.event} has been rated by {self.rating} and t has some suggestion: {self.comments}"

