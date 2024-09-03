from django.db import models
from core.models import Property, Feedback, TimeStampedModel
from lease_rental_management.models import Tenant
from maintenance_and_service_requests.models import MaintenanceRequest, MaintenanceTechnician

class MaintenanceTask(TimeStampedModel):
    TASK_STATUS = (
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(MaintenanceTechnician,on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='assigned')
    start_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def assign_task(self, technician):
        self.assigned_to = technician
        self.status = 'assigned'
        self.start_date = models.DateTimeField(auto_now_add=True)
        self.save()

    def update_task_status(self, status):
        self.status = status
        if status == 'completed':
            self.completion_date = models.DateTimeField(auto_now=True)
        self.save()

    def add_notes(self, note):
        self.notes = note
        self.save()

    def get_task_details(self):
        return {
            'id': self.id,
            'request_id': self.request.id,
            'assigned_to': self.assigned_to.id,
            'status': self.status,
            'start_date': self.start_date,
            'completion_date': self.completion_date,
            'notes': self.notes,
        }

class MaintenanceFeedback(Feedback):
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def submit_feedback(self, rating, comments):
        self.rating = rating
        self.comments = comments
        self.save()

    def get_feedback(self):
        return {
            'request': self.request.id,
            'tenant': self.tenant.username,
            'rating': self.rating,
            'comments': self.comments,
        }

    def get_all_feedback(self, technician):
        feedback_list = MaintenanceFeedback.objects.filter(request__assigned_to=technician)
        return [{
            'tenant': feedback.tenant.username,
            'rating': feedback.rating,
            'comments': feedback.comments,
        } for feedback in feedback_list]

class MaintenanceAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, null=True, blank=True)
    total_requests = models.IntegerField(null=True, blank=True)
    completed_requests = models.IntegerField(null=True, blank=True)
    average_response_time = models.DurationField(null=True, blank=True)
    average_resolution_time = models.DurationField(null=True, blank=True)

    def generate_report(self):
        return {
            'property': self.property.address,
            'period': self.period,
            'total_requests': self.total_requests,
            'completed_requests': self.completed_requests,
            'average_response_time': self.average_response_time,
            'average_resolution_time': self.average_resolution_time,
        }

    def get_trend_analysis(self):
        trend = {
            'total_requests_trend': self.total_requests,
            'completed_requests_trend': self.completed_requests,
        }
        return trend

    def get_performance_metrics(self):
        metrics = {
            'average_response_time': self.average_response_time,
            'average_resolution_time': self.average_resolution_time,
        }
        return metrics

