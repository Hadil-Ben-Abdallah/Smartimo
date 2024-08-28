from django.db import models
from datetime import datetime
from core.models import Document, Notification
from lease_rental_management.models import Tenant

class TenantDocument(Document):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255, blank=True, null=True)
    is_favorite = models.BooleanField(default=False, blank=True, null=True)

    def get_document(self):
        return {
            "tenant": self.tenant.username,
            "tags": self.tags,
            "is_favorite": self.is_favorite,
        }

    def mark_as_favorite(self):
        self.is_favorite = not self.is_favorite
        self.save()
        return self.is_favorite

    def search_documents(self, criteria):
        query = TenantDocument.objects.filter(tenant=self.tenant)
        if 'tags' in criteria:
            query = query.filter(tags__icontains=criteria['tags'])
        if 'date_range' in criteria:
            query = query.filter(created_at__range=criteria['date_range'])
        return query

class DocumentVersion(models.Model):
    document = models.ForeignKey(TenantDocument, on_delete=models.CASCADE)
    version_number = models.IntegerField(blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    changes = models.TextField(blank=True, null=True)

    def get_version_details(self):
        return {
            "document": self.document.document_id,
            "version_number": self.version_number,
            "file_path": self.file_path,
            "upload_date": self.upload_date,
            "changes": self.changes,
        }

    def restore_version(self, version_number):
        previous_version = DocumentVersion.objects.get(document=self.document, version_number=version_number)
        self.document.file_path = previous_version.file_path
        self.document.save()
        return self.document

class DocumentNotification(Notification):
    document = models.ForeignKey(TenantDocument, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def customize_notifications(self, preferences):
        notification_settings = {
            "frequency": preferences.get("frequency", "daily"),
            "delivery_channel": preferences.get("delivery_channel", "email"),
            "document_categories": preferences.get("document_categories", []),
        }
        return notification_settings

