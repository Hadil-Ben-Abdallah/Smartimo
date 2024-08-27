from django.db import models
from core.models import Property, Notification, Feedback
from property_listing.models import PropertyOwner, RealEstateAgent
from django.core.mail import send_mail
from datetime import datetime, timedelta

class VisitorProperty(Property):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    listing_type = models.CharField(max_length=50, choices=[('rental', 'Rental'), ('sale', 'Sale')], default='rental')

    def schedule_showing(self, showing_details):
        showing = Showing.objects.create(property=self, **showing_details)
        return showing

    def get_showings(self):
        return Showing.objects.filter(property=self)

    def update_property_details(self, details):
        for key, value in details.items():
            setattr(self, key, value)
        self.save()

class Visitor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    visit_purpose = models.CharField(max_length=100, choices=[('viewing', 'Viewing'), ('inspecting', 'Inspecting')], default='viewing')

    def check_in(self, property):
        AccessControl.objects.create(property=property, visitor=self, access_code='TEMP_CODE', access_start=datetime.now(), access_end=datetime.now() + timedelta(hours=1), permissions={})

    def check_out(self, property):
        access = AccessControl.objects.filter(property=property, visitor=self).last()
        if access:
            access.access_end = datetime.now()
            access.save()

    def provide_feedback(self, feedback):
        Feedback.objects.create(visitor=self, **feedback)

class Showing(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(VisitorProperty, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])

    def send_invitation(self):
        subject = "Property Showing Invitation"
        message = f"You have been invited to a property showing on {self.date} at {self.time}. Property ID: {self.property.property_id}"
        recipient_list = [self.visitor.email]
        send_mail(subject, message, 'smartimo@example.com', recipient_list)

    def send_reminder(self):
        from django.core.mail import send_mail
        subject = "Reminder: Property Showing"
        message = f"This is a reminder for your property showing on {self.date} at {self.time}. Property ID: {self.property.property_id}"
        recipient_list = [self.visitor.email]
        send_mail(subject, message, 'smartimo@example.com', recipient_list)

    def update_showing_details(self, details):
        for key, value in details.items():
            setattr(self, key, value)
        self.save()

    def cancel_showing(self):
        self.status = 'cancelled'
        self.save()


class AccessControl(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(VisitorProperty, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    access_code = models.CharField(max_length=50)
    access_start = models.DateTimeField()
    access_end = models.DateTimeField()
    permissions = models.JSONField()
    
    def grant_access(self, details):
        for key, value in details.items():
            setattr(self, key, value)
        self.save()

    def revoke_access(self):
        self.delete()

    def update_access_details(self, details):
        for key, value in details.items():
            setattr(self, key, value)
        self.save()


class VisitorFeedback(Feedback):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    property = models.ForeignKey(VisitorProperty, on_delete=models.CASCADE)
    
    def submit_feedback(self, details):
        Feedback.objects.create(visitor=self.visitor, property=self.property, **details)

    def get_feedback(self, property):
        return Feedback.objects.filter(property=property)



class VisitorNotification(Notification):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[('reminder', 'Reminder'), ('alert', 'Alert')], default='reminder')
    
    def update_status(self, status):
        self.status = status
        self.save()

    def view_notification_history(self, visitor):
        return VisitorNotification.objects.filter(visitor=visitor)