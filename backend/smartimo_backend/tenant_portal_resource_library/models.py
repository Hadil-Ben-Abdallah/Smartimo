from django.db import models
from core.models import Resource, Feedback, TimeStampedModel
from lease_rental_management.models import Tenant

class TenantPortalResource(Resource):
    category = models.CharField(max_length=255, choices=[('property_care', 'Property Care'), ('community_guidelines', 'Community Guidelines'), ('local_services', 'Local Services')], default='property_care')
    content_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video')], default='text')
    file_url = models.URLField(blank=True, null=True)

    def add_resource(self, title, description, contact_info, category, content_type, file_url):
        self.title = title
        self.description = description
        self.contact_info = contact_info
        self.category = category
        self.content_type = content_type
        self.file_url = file_url
        self.save()
        return self

    def update_resource(self, resource_id, title=None, description=None, contact_info=None, category=None, content_type=None, file_url=None):
        resource = TenantPortalResource.objects.get(id=resource_id)
        if title:
            resource.title = title
        if description:
            resource.description = description
        if contact_info:
            resource.contact_info = contact_info
        if category:
            resource.category = category
        if content_type:
            resource.content_type = content_type
        if file_url:
            resource.file_url = file_url
        resource.save()
        return resource

    def delete_resource(self):
        self.delete()

    def get_resource(self, resource_id):
        return TenantPortalResource.objects.get(id=resource_id)

    def list_resources(self, category=None):
        if category:
            return TenantPortalResource.objects.filter(category=category)
        return TenantPortalResource.objects.all()

class LocalService(Resource):
    category = models.CharField(max_length=255, choices=[('dining', 'Dining'), ('healthcare', 'Healthcare')], default='dining')
    rating = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def add_service(self, title, description, contact_info,category, rating, address):
        self.title = title
        self.description = description
        self.contact_info = contact_info
        self.category = category
        self.rating = rating
        self.address = address
        self.save()
        return self

    def update_service(self, service_id, title=None, description=None, contact_info=None, category=None, rating=None, address=None):
        service = LocalService.objects.get(id=service_id)
        if title:
            service.title = title
        if description:
            service.description = description
        if contact_info:
            service.contact_info = contact_info
        if category:
            service.category = category
        if rating:
            service.rating = rating
        if address:
            service.address = address
        service.save()
        return service

    def delete_service(self):
        self.delete()

    def get_service(self, service_id):
        return LocalService.objects.get(id=service_id)

    def list_services(self, category=None):
        if category:
            return LocalService.objects.filter(category=category)
        return LocalService.objects.all()

class TenantPortalFeedback(Feedback):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    resource = models.ForeignKey(TenantPortalResource, on_delete=models.CASCADE)

    def submit_feedback(self, rating, comments, tenant_id, resource_id):
        self.rating = rating
        self.comments = comments
        self.tenant.user_id = tenant_id
        self.resource.resource_id = resource_id
        self.save()
        return self

    def update_feedback(self, feedback_id, rating=None, comments=None, tenant=None, resource=None):
        feedback = TenantPortalFeedback.objects.get(id=feedback_id)
        if rating:
            feedback.rating = rating
        if comments:
            feedback.comments = comments
        if tenant:
            feedback.tenant.user_id = tenant
        if resource:
            feedback.resource = resource
        feedback.save()
        return feedback

    def get_feedback(self, feedback_id):
        return TenantPortalFeedback.objects.get(id=feedback_id)

    def list_feedback(self, resource_id=None):
        if resource_id:
            return TenantPortalFeedback.objects.filter(resource_id=resource_id)
        return TenantPortalFeedback.objects.all()

class ContentManagement(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    resource_updates = models.JSONField(default=dict, blank=True, null=True)
    feedback_reviews = models.JSONField(default=dict, blank=True, null=True)

    def review_feedback(self, feedback_id, action_taken):
        feedback = TenantPortalFeedback.objects.get(id=feedback_id)
        self.feedback_reviews[feedback_id] = action_taken
        self.save()

    def manage_resources(self, resource_id, update_data):
        resource = TenantPortalResource.objects.get(id=resource_id)
        if 'category' in update_data:
            resource.category = update_data['category']
        if 'content_type' in update_data:
            resource.content_type = update_data['content_type']
        if 'file_url' in update_data:
            resource.file_url = update_data['file_url']
        resource.save()
        return resource

    def track_changes(self, resource_id):
        return self.resource_updates.get(str(resource_id), {})

    def communicate_updates(self):
        pass

