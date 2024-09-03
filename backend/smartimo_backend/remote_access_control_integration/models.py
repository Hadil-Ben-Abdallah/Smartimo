from django.db import models
from core.models import Property, User, TimeStampedModel
from lease_rental_management.models import Tenant
from tenant_portal_development.models import TenantPortal

class RemoteAccessControlSystem(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    system_type = models.CharField(max_length=100, choices=[('keyless_entry', 'Keyless Entry'), ('digital_locks', 'Digital Locks')], default='keyless_entry')
    integration_status = models.CharField(max_length=50, choices=[('connected', 'Connected'), ('disconnected', 'Disconnected')], default='connected')

    def connect_to_platform(self):
        self.integration_status = 'connected'
        self.save()
        return "Connected to platform"

    def configure_permissions(self, permissions: dict):
        return "Permissions configured"

    def get_access_status(self):
        return {
            'status': 'online',
            'logs': []
        }

class AccessPermission(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=50, choices=[('full_access', 'Full Access'), ('restricted_access', 'Restricted Access')])
    time_window = models.CharField(max_length=50, blank=True, null=True)
    entry_point = models.CharField(max_length=100, blank=True, null=True)

    def grant_access(self, user: User, property: Property):
        self.user.user_id = user
        self.property.property_id = property
        self.save()
        return "Access granted"

    def set_restrictions(self, restrictions: dict):
        self.time_window = restrictions.get('time_window', self.time_window)
        self.save()
        return "Restrictions set"

    def revoke_access(self, user: User):
        if self.user.user_id == user:
            self.delete()
            return "Access revoked"
        return "User does not have access"

class RemoteTenantPortal(TenantPortal):
    access_permissions = models.ManyToManyField(AccessPermission)

    def view_permissions(self):
        return {
            'permissions': list(self.access_permissions.values())
        }

    def grant_temporary_access(self, visitor: User, access_code: str):
        permission = AccessPermission(
            user_id=visitor,
            access_level='temporary',
            time_window='limited',
            entry_point='main_door'
        )
        permission.save()
        return "Temporary access granted"

    def receive_notifications(self):
        return {
            'notifications': []
        }

class ServiceProvider(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    contact_information = models.JSONField(blank=True, null=True)

    def request_access(self, property: Property):
        return "Access request submitted"

    def receive_access_instructions(self):
        return {
            'instructions': []
        }

class RemoteMaintenanceRequest(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed')], default='pending')
    access_instructions = models.TextField(blank=True, null=True)

    def submit_request(self, service_provider: ServiceProvider):
        self.service_provider = service_provider
        self.status = 'pending'
        self.save()
        return "Request submitted"

    def update_request_status(self, status: str):
        self.status = status
        self.save()
        return "Status updated"

    def view_access_instructions(self):
        return {
            'access_instructions': self.access_instructions
        }

class PropertyOwnerDashboard(TimeStampedModel):
    owner_id = models.AutoField(primary_key=True)
    properties = models.ManyToManyField(Property)
    access_control_data = models.JSONField(blank=True, null=True)

    def monitor_access_status(self):
        return {
            'access_status': []
        }

    def adjust_access_settings(self, property: Property, settings: dict):
        return "Access settings adjusted"

    def generate_access_reports(self):
        return {
            'reports': []
        }

class RemoteProperty(Property):
    access_points = models.JSONField(blank=True, null=True)
    tenants = models.ManyToManyField(Tenant, related_name='tenant_properties')

    def update_access_points(self, points: list):
        self.access_points = points
        self.save()
        return "Access points updated"

    def get_access_point_status(self):
        return {
            'access_points': self.access_points
        }

