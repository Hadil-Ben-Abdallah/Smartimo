from django.db import models
from core.models import User, Property, Document, Reminder, Category
from django.utils import timezone

class PropertyDocument(Document):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def get_document_details(self):
        return {
            "id": self.document_id,
            "document_type": self.document_type,
            "file_path": self.file_path,
            "property_id": self.property.property_id,
            "uploaded_by": self.uploaded_by,
            "uploaded_at": self.uploaded_at,
            "access_permissions": self.access_permissions,
            "expiration_date": self.expiration_date
        }
    
    def set_expiration_reminder(self, expiration_date):
        self.expiration_date = expiration_date
        self.save()

class DocumentCategory(Category):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def create_category(self, name, description, property):
        self.property.property_id = property
        self.save()

    def get_category_details(self):
        return {
            "property": self.property.property_id
        }

class DocumentTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    document = models.ForeignKey(PropertyDocument, on_delete=models.CASCADE)

    def create_tag(self, name):
        self.name = name
        self.save()
    
    def update_tag(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def delete_tag(self):
        self.delete()
    
    def get_tag_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "document_id": self.document.document_id,
        }

class DocumentExpirationReminder(Reminder):
    document = models.ForeignKey(PropertyDocument, on_delete=models.CASCADE)

    
    def get_reminder_details(self):
        return {
            "id": self.reminder_id,
            "document_id": self.document.document_id,
            "message_content": self.message_content,
            "reminder_date": self.reminder_date,
            "frequency": self.frequency,
            "delivary_channel": self.delivary_channel,
            "status": self.status,
        }

class DocumentSharing(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(PropertyDocument, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    access_permissions = models.JSONField(default=dict)
    activity_log = models.JSONField(default=list)

    def share_document(self, document_id, shared_with, access_permissions):
        self.document_id = document_id
        self.shared_with = shared_with
        self.access_permissions = access_permissions
        self.save()
    
    def update_permissions(self, permissions):
        self.access_permissions = permissions
        self.save()
    
    def revoke_access(self):
        self.delete()
    
    def log_activity(self, activity):
        self.activity_log.append(activity)
        self.save()

class ESignatureIntegration(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(PropertyDocument, on_delete=models.CASCADE)
    signature_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    signed_at = models.DateTimeField(null=True, blank=True)
    signing_party = models.ForeignKey(User, on_delete=models.CASCADE)
    signature_log = models.JSONField(default=list)

    def initiate_signature(self, document_id, signing_party):
        self.document_id = document_id
        self.signing_party = signing_party
        self.signature_status = 'initiated'
        self.save()
    
    def update_signature_status(self, status):
        self.signature_status = status
        if status == 'signed':
            self.signed_at = timezone.now()
        self.save()
    
    def log_signature_activity(self, activity):
        self.signature_log.append(activity)
        self.save()
    
    def get_signature_details(self):
        return {
            "id": self.id,
            "document_id": self.document_id,
            "signature_status": self.signature_status,
            "signed_at": self.signed_at,
            "signing_party": self.signing_party,
            "signature_log": self.signature_log,
        }

