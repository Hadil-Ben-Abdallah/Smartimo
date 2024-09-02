from django.db import models
from core.models import User, Property, Communication, TimeStampedModel
from lease_rental_management.models import Tenant

class Complaint(TimeStampedModel):
    COMPLAINT_CATEGORIES = [
        ('maintenance', 'Maintenance'),
        ('noise', 'Noise'),
        ('neighbor_dispute', 'Neighbor Dispute'),
    ]

    URGENCY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=COMPLAINT_CATEGORIES, default='maintenance')
    description = models.TextField(blank=True, null=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    attachments = models.JSONField(default=list, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def submit_complaint(self):
        self.status = 'submitted'
        self.save()
        return self

    def update_status(self, status: str):
        self.status = status
        if status == 'resolved':
            self.resolved_at = models.DateTimeField(auto_now=True)
        self.save()
        return self

    def add_attachment(self, file: str):
        self.attachments.append(file)
        self.save()
        return self

    def get_details(self):
        return {
            "complaint_id": self.id,
            "tenant_id": self.tenant.user_id,
            "category": self.category,
            "description": self.description,
            "urgency": self.urgency,
            "status": self.status,
            "attachments": self.attachments,
            "submitted_at": self.submitted_at,
            "resolved_at": self.resolved_at,
        }

class ComplaintTicket(TimeStampedModel):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    id = models.AutoField(primary_key=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    due_date = models.DateField(blank=True, null=True)

    def assign_to_user(self, user_id: int):
        self.assigned_to = user_id
        self.save()
        return self

    def update_status(self, status: str):
        self.status = status
        self.save()
        return self

    def set_due_date(self, date: str):
        self.due_date = date
        self.save()
        return self

    def get_ticket_details(self):
        return {
            "ticket_id": self.id,
            "complaint_id": self.complaint.id,
            "assigned_to": self.assigned_to.user_id,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
        }

class SatisfactionCommunication(Communication):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    sender = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_communication_history(self):
        history = SatisfactionCommunication.objects.filter(complaint_id=self.complaint_id)
        return [
            {
                "sender": comm.sender.user_id,
                "recipient": comm.recipient.user_id,
            }
            for comm in history
        ]

class ComplaintAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def record_metric(self, value: float):
        self.value = value
        self.save()
        return self

    def generate_report(self):
        return {
            "property_id": self.property.property_id,
            "metric_name": self.metric_name,
            "value": self.value,
            "generated_at": models.DateTimeField(auto_now=True),
        }

    def analyze_trends(self):
        trend_data = ComplaintAnalytics.objects.filter(property=self.property.property_id)
        return list(trend_data.values('metric_name', 'value'))

class ComplaintProperty(Property):
    tenant_list = models.ManyToManyField(Tenant, blank=True, null=True)
    complaints = models.ManyToManyField(Complaint, blank=True, null=True)

    def view_complaints(self):
        return list(self.complaints.values('complaint_id', 'description', 'status'))

    def add_tenant(self, tenant: Tenant):
        self.tenant_list.add(tenant)
        self.save()
        return self

    def get_property_details(self):
        return {
            "tenant_list": list(self.tenant_list.values('user_id', 'username')),
            "complaints": list(self.complaints.values('id', 'description', 'status')),
        }

