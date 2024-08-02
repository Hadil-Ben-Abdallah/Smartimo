from django.db import models
from django.contrib.auth.models import User
from core.models import Property
from django.utils import timezone

class PropertyDocument(models.Model):
    DOCUMENT_TYPES = (
        ('contract', 'Contract'),
        ('agreement', 'Agreement'),
        ('deed', 'Deed'),
        ('inspection_report', 'Inspection Report'),
        ('insurance_policy', 'Insurance Policy'),
    )
    
    id = models.AutoField(primary_key=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file_path = models.CharField(max_length=255)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    access_permissions = models.JSONField(default=dict)
    expiration_date = models.DateField(null=True, blank=True)

    def upload_document(self, file_path):
        self.file_path = file_path
        self.save()
    
    def update_document(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def set_permissions(self, permissions):
        self.access_permissions = permissions
        self.save()
    
    def get_document_details(self):
        return {
            "id": self.id,
            "document_type": self.document_type,
            "file_path": self.file_path,
            "property_id": self.property_id,
            "uploaded_by": self.uploaded_by,
            "uploaded_at": self.uploaded_at,
            "access_permissions": self.access_permissions,
            "expiration_date": self.expiration_date
        }
    
    def set_expiration_reminder(self, expiration_date):
        self.expiration_date = expiration_date
        self.save()

class DocumentCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)

    def create_category(self, name, description):
        self.name = name
        self.description = description
        self.save()
    
    def update_category(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def delete_category(self):
        self.delete()
    
    def get_category_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "property_id": self.property_id,
        }

class DocumentTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    document_id = models.ForeignKey(PropertyDocument, on_delete=models.CASCADE)

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
            "document_id": self.document_id,
        }

class DocumentExpirationReminder(models.Model):
    id = models.AutoField(primary_key=True)
    document_id = models.ForeignKey(PropertyDocument, on_delete=models.CASCADE)
    reminder_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('sent', 'Sent')], default='pending')

    def create_reminder(self, reminder_date):
        self.reminder_date = reminder_date
        self.save()
    
    def update_reminder(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def send_reminder(self):
        self.status = 'sent'
        self.save()
    
    def get_reminder_details(self):
        return {
            "id": self.id,
            "document_id": self.document_id,
            "reminder_date": self.reminder_date,
            "status": self.status,
        }

class DocumentSharing(models.Model):
    id = models.AutoField(primary_key=True)
    document_id = models.ForeignKey(PropertyDocument, on_delete=models.CASCADE)
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
    document_id = models.ForeignKey(PropertyDocument, on_delete=models.CASCADE)
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

