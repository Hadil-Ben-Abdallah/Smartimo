from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from core.models import User, Notification, Property
from client_management.models import Client

class Email(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachments = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, choices=[('sent', 'Sent'), ('received', 'Received'), ('draft', 'Draft')])

    def send_email(self):
        subject = f"{self.subject}"
        message = (
            f"Dear {self.recipient.name},\n\n"
            f"{self.body}\n\n"
            f"below you will find the necessary documents"
            f"From:\n{self.sender}\n\n"
            f"Thank you,\nThe Smartimo Team\n\n"
            f"{self.attachments}"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL)
        return f"The email {self.id} has been sent successfully."


    def save_draft(self):
        self.status = 'draft'
        self.save()

    def attach_files(self, files):
        self.attachments.extend(files)
        self.save()

    def organize_emails(self, folder_name):
        pass

    def get_email_details(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "recipient": self.recipient.username,
            "subject": self.subject,
            "body": self.body,
            "attachments": self.attachments,
            "timestamp": self.timestamp,
            "status": self.status
        }

class CommunicationNotification(Notification):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    type = models.CharField(max_length=50, choices=[('lease_renewal', 'Lease Renewal'), ('maintenance_schedule', 'Maintenance Schedule')])

    def schedule_notification(self, schedule_time):
        # Schedule automated notifications
        pass

    def customize_template(self, template):
        # This would involve storing and applying templates to notifications
        pass

    def track_delivery(self):
        pass

    def get_notification_details(self):
        return {
            "id": self.notification_id,
            "sender": self.sender.username,
            "recipient": self.recipient.username,
            "message": self.message,
            "type": self.type
        }

class InstantMessage(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_instant_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_instant_messages')
    content = models.TextField()
    attachments = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, choices=[('sent', 'Sent'), ('read', 'Read')])

    def send_message(self):
        pass

    def create_group_chat(self, participants):
        pass

    def share_files(self, files):
        self.attachments.extend(files)
        self.save()

    def archive_message(self):
        pass

    def search_messages(self, query):
        pass

class SMSNotification(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_sms_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_sms_notifications')
    message = models.TextField()
    status = models.CharField(max_length=50, choices=[('sent', 'Sent'), ('delivered', 'Delivered')])

    def send_sms(self):
        pass

    def schedule_sms(self, schedule_time):
        pass

    def customize_sms_template(self, template):
        # This would involve storing and applying SMS templates
        pass

    def track_sms_delivery(self):
        pass

    def get_sms_details(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "recipient": self.recipient.username,
            "message": self.message,
            "timestamp": self.timestamp,
            "status": self.status
        }

class CommunicationLog(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    communication_type = models.CharField(max_length=50, choices=[('email', 'Email'), ('instant_message', 'Instant Message'), ('sms', 'SMS')])

    def log_communication(self):
        self.save()

    def view_communication_history(self):
        return CommunicationLog.objects.filter(client=self.client, property=self.property).order_by('-id')

    def search_communication_logs(self, query):
        return CommunicationLog.objects.filter(message__icontains=query)

    def filter_communication_logs(self, criteria):
        return CommunicationLog.objects.filter(**criteria)


    def get_log_details(self):
        return {
            "id": self.id,
            "client": self.client if self.client else None,
            "property": self.property.property_id if self.property else None,
            "communication_type": self.communication_type
        }

