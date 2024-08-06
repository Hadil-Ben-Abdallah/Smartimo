from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.core.files.storage import default_storage
import json
from core.models import User, Property
from property_listing.models import RealEstateAgent


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, related_name='appointments_as_agent', on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name='appointments_as_client', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    details = models.TextField()

    def schedule_appointment(self):
        return f"Appointment scheduled for {self.id}."

    def send_confirmation(self):
        subject = f"Appointment Confirmation - {self.id}"
        message = (
            f"Dear {self.client.name},\n\n"
            f"Your appointment for property {self.property} with agent {self.agent} "
            f"on {self.date} at {self.time} has been confirmed.\n\n"
            f"Details:\n{self.details}\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [self.client.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Confirmation sent for appointment {self.id}."

    def send_reminders(self):
        subject = f"Appointment Reminder - {self.id}"
        message = (
            f"Dear {self.client.name},\n\n"
            f"This is a reminder for your upcoming appointment with agent {self.agent.id} "
            f"on {self.date} at {self.time} for property {self.property.id}.\n\n"
            f"Details:\n{self.details}\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [self.client.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Reminders sent for appointment {self.id}."


class Inspection(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='inspections', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    checklist = models.JSONField()
    status = models.CharField(max_length=50)
    report = models.FileField(upload_to='inspection_reports/', null=True, blank=True)

    def schedule_inspection(self):
        return f"Inspection scheduled for {self.id}."

    def send_reminders(self):
        subject = f"Inspection Reminder - {self.id}"
        message = (
            f"Dear {self.manager.name},\n\n"
            f"This is a reminder for the upcoming inspection of property {self.property.id} "
            f"scheduled for {self.date} at {self.time}.\n\n"
            f"Checklist:\n{json.dumps(self.checklist, indent=2)}\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [self.manager.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Reminders sent for inspection {self.id}."

    def document_findings(self, findings_text, report_file):
        report_path = default_storage.save(f'inspection_reports/{self.id}_report.pdf', report_file)
        self.report.name = report_path
        self.save()

        findings_path = default_storage.save(f'inspection_reports/{self.id}_findings.txt', findings_text)

        return f"Findings documented for inspection {self.id}."


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=50, choices= [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default= 'low')
    deadline = models.DateTimeField()
    status = models.CharField(max_length=50, choices= [('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default= 'pending')
    category = models.CharField(max_length=50, choices= [('sales', 'Sales'), ('rental', 'Rental'), ('maintenance', 'Maintenance')], default= 'sales')

    def create_task(self):
        return f"Task created with ID {self.id}."

    def update_status(self):
        return f"Task {self.id} status updated to {self.status}."

    def set_priority(self):
        return f"Task {self.id} priority set to {self.priority}."

    def get_task_details(self):
        return f"Task Details - ID: {self.id}, Title: {self.title}, Description: {self.description}, Priority: {self.priority}, Deadline: {self.deadline}, Status: {self.status}, Category: {self.category}."

    def send_reminders(self):
        subject = f"Reminder for Task ID {self.id}"
        message = (
            f"Dear {self.user.name},\n\n"
            f"This is a reminder for your task '{self.title}' with priority '{self.priority}'.\n\n"
            f"Description:\n{self.description}\n\n"
            f"Deadline: {self.deadline}\n"
            f"Status: {self.status}\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [self.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Reminders sent for task {self.id}."


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    organizer = models.ForeignKey(User, related_name='meetings_organized', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='meetings_participated')
    date = models.DateField()
    time = models.TimeField()
    topic = models.CharField(max_length=255)
    agenda = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices= [('scheduled', 'Scheduled'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default= 'pending')

    def schedule_meeting(self):
        return f"Meeting scheduled with ID {self.id}."

    def send_invitations(self):
        subject = f"Meeting Invitation - {self.id}"
        message = (
            f"Dear participants,\n\n"
            f"You are invited to a meeting on {self.date} at {self.time}.\n\n"
            f"Topic: {self.topic}\n"
            f"Agenda:\n{self.agenda}\n"
            f"Location: {self.location}\n\n"
            f"Please RSVP at your earliest convenience.\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [user.email for user in self.participants.all()]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Invitations sent for meeting {self.id}."

    def track_rsvps(self):
        rsvps = {user.id: "Confirmed" for user in self.participants.all()}
        return f"RSVPs tracked for meeting {self.id}."

    def send_reminders(self):
        subject = f"Meeting Reminder - {self.id}"
        message = (
            f"Dear participants,\n\n"
            f"This is a reminder for our upcoming meeting on {self.date} at {self.time}.\n\n"
            f"Topic: {self.topic}\n"
            f"Agenda:\n{self.agenda}\n"
            f"Location: {self.location}\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [user.email for user in self.participants.all()]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Reminders sent for meeting {self.id}."


class CalendarIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar_service = models.CharField(max_length=50)
    sync_status = models.CharField(max_length=50, choices= [('active', 'Active'), ('inactive', 'Inactive')], default= 'active')
    last_sync = models.DateTimeField(null=True, blank=True)

    def integrate_calendar(self):
        return f"Integrated with {self.calendar_service}."

    def sync_appointments(self):
        if self.sync_status == 'active':
            sync_status = "success" 
            if sync_status == "success":
                self.last_sync = timezone.now()
                self.save()
                return f"Appointments synced with {self.calendar_service}."
            else:
                return f"Failed to sync appointments with {self.calendar_service}."
        else:
            return "Calendar integration is inactive."

    def update_sync_status(self):
        return f"Sync status updated to {self.sync_status}."

    def get_sync_details(self):
        return f"Sync Details - Calendar Service: {self.calendar_service}, Sync Status: {self.sync_status}, Last Sync: {self.last_sync}."
