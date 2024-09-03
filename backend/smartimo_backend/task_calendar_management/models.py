from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.core.files.storage import default_storage
import json
from core.models import User, Property, TimeStampedModel
from property_listing.models import RealEstateAgent


class Appointment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, related_name='appointments_as_agent', on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name='appointments_as_client', on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def schedule_appointment(self):
        return f"Appointment scheduled for {self.id}."

    def send_confirmation(self):
        subject = f"Appointment Confirmation - {self.id}"
        message = (
            f"Dear {self.client.username},\n\n"
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
            f"Dear {self.client.username},\n\n"
            f"This is a reminder for your upcoming appointment with agent {self.agent.user_id} "
            f"on {self.date} at {self.time} for property {self.property.property_id}.\n\n"
            f"Details:\n{self.details}\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [self.client.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Reminders sent for appointment {self.id}."


class Inspection(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='inspections', on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    checklist = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    report = models.FileField(upload_to='inspection_reports/', null=True, blank=True)

    def schedule_inspection(self):
        return f"Inspection scheduled for {self.id}."

    def send_reminders(self):
        subject = f"Inspection Reminder - {self.id}"
        message = (
            f"Dear {self.manager.username},\n\n"
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


class Task(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=50, choices= [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default= 'low')
    deadline = models.DateTimeField(blank=True, null=True)
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
            f"Dear {self.user.username},\n\n"
            f"This is a reminder for your task '{self.title}' with priority '{self.priority}'.\n\n"
            f"Description:\n{self.description}\n\n"
            f"Deadline: {self.deadline}\n"
            f"Status: {self.status}\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [self.user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Reminders sent for task {self.id}."
    

class TaskManager(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)
    calendar = models.JSONField(default=dict, blank=True, null=True)
    reminders = models.JSONField(default=list, blank=True, null=True)

    def add_task(self, task):
        self.tasks.append(task)
        self.save()
        return f"Task '{task}' has been added."

    def update_task(self, task_id, updated_task):
        self.tasks[task_id] = updated_task
        self.save()
        return f"Task {task_id} has been updated."

    def set_reminder(self, task_id, reminder_time):
        self.reminders.append({"task_id": task_id, "time": reminder_time})
        self.save()
        return f"Reminder set for task {task_id} at {reminder_time}."

class Event(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    organizer = models.ForeignKey(User, related_name='events_organized', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='events_participated')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices= [('scheduled', 'Scheduled'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default= 'pending')

    def schedule_event(self):
        return f"event scheduled with ID {self.id}."

    def send_invitations(self):
        subject = f"Event Invitation - {self.id}"
        message = (
            f"Dear participants,\n\n"
            f"You are invited to a event on {self.date} at {self.time}.\n\n"
            f"Topic: {self.topic}\n"
            f"Location: {self.location}\n\n"
            f"Please RSVP at your earliest convenience.\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [User.email for user in self.participants.all()]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Invitations sent for event {self.id}."

    def track_rsvps(self):
        rsvps = {User.user_id: "Confirmed" for user in self.participants.all()}
        return f"RSVPs tracked for event {self.id}."

    def send_reminders(self):
        subject = f"Event Reminder - {self.id}"
        message = (
            f"Dear participants,\n\n"
            f"This is a reminder for our upcoming event on {self.date} at {self.time}.\n\n"
            f"Topic: {self.topic}\n"
            f"Location: {self.location}\n\n"
            f"Thank you,\nThe Smartimo Team"
        )
        recipient_list = [User.email for user in self.participants.all()]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Reminders sent for event {self.id}."


class CalendarIntegration(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar_service = models.CharField(max_length=50, blank=True, null=True)
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
