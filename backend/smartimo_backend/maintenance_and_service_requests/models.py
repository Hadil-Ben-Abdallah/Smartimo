from django.db import models
from django.utils import timezone
from core.models import Notification, Property
from lease_rental_management.models import PropertyManager, Tenant

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='maintenance_requests')
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE, related_name='agreements')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='properties')
    issue_type = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField()
    photos = models.JSONField(default=list)
    urgency_level = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    submission_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(auto_now=True)

    def submit_request(self):
        property_manager = self.get_property_manager()

        if property_manager:
            MaintenanceNotification.objects.create(
                recipient_id=property_manager.user_id,
                type='new_request',
                message=f'New maintenance request submitted by tenant {self.tenant.username}. Issue: {self.issue_type}.'
            )

    def get_property_manager(self):
        return self.manager

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.updated_at = timezone.now()
            self.save()
            MaintenanceNotification.objects.create(
                recipient_id=self.tenant.username,
                type='status_update',
                message=f'Your maintenance request has been updated to {new_status}.'
            )

    def add_notes_photos(self, notes, photos):
        self.description += f'\nNotes: {notes}'
        self.photos.extend(photos)
        self.save()

    def create_request(self, tenant, manager, issue_type, location, description, severity, photos, urgency_level):
        self.tenant = tenant
        self.manager = manager
        self.issue_type = issue_type
        self.severity = severity
        self.location = location
        self.description = description
        self.photos = photos
        self.status = 'Pending'
        self.urgency_level = urgency_level
        self.save()

    def get_request_details(self):
        return {
            "id": self.id,
            "tenant": self.tenant.user_id,
            "manager": self.manager.user_id,
            "issue_type": self.issue_type,
            "severity": self.severity,
            "location": self.location,
            "description": self.description,
            "photos": self.photos,
            "status": self.status,
        }

    def delete_request(self):
        self.delete()

class TenantRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant_requests')
    unit_number = models.CharField(max_length=50)
    maintenance_requests = models.ManyToManyField(MaintenanceRequest, related_name='tenant_requests')

    def view_requests(self):
        return self.maintenance_requests.all()

    def receive_notifications(self):
        return MaintenanceNotification.objects.filter(recipient_id=self.tenant)

    def rate_service(self, request_id, rating):
        pass

class MaintenancePropertyManager(models.Model):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE, related_name='property_managers')
    assigned_requests = models.ManyToManyField(MaintenanceRequest, related_name='assigned_requests')

    def view_requests_dashboard(self):
        return self.assigned_requests.all()

    def prioritize_requests(self):
        return self.assigned_requests.order_by('severity')

    def assign_tasks(self, request_id):
        request = MaintenanceRequest.objects.get(id=request_id)
        request.status = 'in_progress'
        request.save()
        MaintenanceNotification.objects.create(
            recipient_id=MaintenanceTechnician.id,
            type='task_assignment',
            message=f'New task assigned: {request.issue_type} at {request.location}.'
        )

    def track_performance(self):
        return {
            "total_requests": self.assigned_requests.count(),
            "completed_requests": self.assigned_requests.filter(status='completed').count(),
            "average_resolution_time": self._calculate_average_resolution_time()
        }

    def _calculate_average_resolution_time(self):
        # total_time = 0
        # completed_requests = self.assigned_requests.filter(status='completed')
        # for request in completed_requests:
        #     if request.created_at and request.updated_at:
        #         total_time += (request.updated_at - request.created_at).total_seconds()
        # count = completed_requests.count()
        # return total_time / count if count > 0 else 0
        pass

    def generate_reports(self):
        return {
            "requests": self.track_performance(),
        }

class MaintenanceTechnician(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    skills = models.TextField()
    assigned_tasks = models.ManyToManyField(MaintenanceRequest, related_name='technicians')

    def view_assigned_tasks(self):
        return self.assigned_tasks.all()

    def update_task_status(self, request_id, new_status):
        request = MaintenanceRequest.objects.get(id=request_id)
        request.update_status(new_status)
        MaintenanceNotification.objects.create(
            recipient_id=request.tenant.user_id,
            type='status_update',
            message=f'The status of your request {request_id} has been updated to {new_status}.'
        )

    def add_repair_notes(self, request_id, notes, photos):
        request = MaintenanceRequest.objects.get(id=request_id)
        request.add_notes_photos(notes, photos)

    def get_task_details(self, request_id):
        request = MaintenanceRequest.objects.get(id=request_id)
        return request.get_request_details()

class MaintenanceNotification(Notification):
    recipient_id = models.IntegerField()  # Can be tenant or property manager or technicien id
    type = models.CharField(max_length=50)

    def track_delivery_status(self):
        pass

    def get_notification_history(self):
        return MaintenanceNotification.objects.filter(recipient_id=self.recipient_id)

    class Meta:
        abstract = True
