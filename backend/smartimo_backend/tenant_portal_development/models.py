from django.db import models
from core.models import Notification, Resource, Portal
from lease_rental_management.models import Tenant

class TenantPortal(Portal):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

class TenantNotification(Notification):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=[('lease_renewal', 'Lease Renewal'), ('rent_increase', 'Rent Increase')], default='lease_renewal')
    delivery_method = models.CharField(max_length=50, choices=[('email', 'Email'), ('sms', 'SMS')], default='email')
    frequency = models.CharField(max_length=50)

    def customize_preferences(self, new_preferences):
        self.frequency = new_preferences.get('frequency', self.frequency)
        self.delivery_method = new_preferences.get('delivery_method', self.delivery_method)
        self.save()
        return "Preferences updated"

    def view_notification_history(self):
        return list(TenantNotification.objects.filter(tenant=self.tenant))

class TenantResource(Resource):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def access_resource(self, resource_id):
        try:
            resource = TenantResource.objects.get(id=resource_id)
            return resource
        except TenantResource.DoesNotExist:
            return "Resource not found"

    def subscribe_to_updates(self, resource_id: int):
        try:
            # Fetch the resource based on resource_id
            resource = TenantResource.objects.get(id=resource_id, tenant=self.tenant)

            resource.add_subscriber(self.tenant)
            
            return "Successfully subscribed to updates for this resource."
    
        except TenantResource.DoesNotExist:
            return "Resource not found or you do not have access to this resource."


    def view_announcements(self):
        pass
