from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Document, Notification
from lease_rental_management.models import Tenant, PropertyManager

class PortfolioDocument(Document):
    category = models.CharField(max_length=255, choices=[('lease', 'Lease'), ('contract', 'Contract'), ('maintenance_record', 'Maintenance Record')], default='lease')
    metadata = models.JSONField(blank=True, null=True)

    def delete_document(self):
        self.delete()

    def get_document(self):
        return {
            'id': self.document_id,
            'title': self.title,
            'document_type': self.document_type,
            'file_path': self.file_path,
            'description': self.description,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at,
            'version': self.version,
            'access_permissions': self.access_permissions,
            'expiration_date': self.expiration_date,
            'category': self.category,
            'metadata': self.metadata,
        }

    def update_documents(self, title=None, document_type=None, file_path=None, description=None, uploaded_by=None, uploaded_at=None, version=None, access_permissions=None, expiration_date=None, category=None, metadata=None):
        if title:
            self.title = title
        if document_type:
            self.document_type = document_type
        if file_path:
            self.file_path = file_path
        if description:
            self.description = description
        if uploaded_by:
            self.uploaded_by = uploaded_by
        if uploaded_at:
            self.uploaded_at = uploaded_at
        if version:
            self.version = version
        if access_permissions:
            self.access_permissions = access_permissions
        if expiration_date:
            self.expiration_date = expiration_date
        if category:
            self.category = category
        if metadata:
            self.metadata = metadata
        self.save()
        return self
    
    def list_documents(cls, filters=None):
        if filters:
            return cls.objects.filter(**filters)
        return cls.objects.all()


class DocumentAccessPermission(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255, choices=[('property_manager', 'Property Manager'), ('owner', 'Owner'), ('administrator' ,'Administrator')], default='property_manager')
    document = models.ForeignKey(PortfolioDocument, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=255, choices=[('view', 'View'), ('edit', 'Edit'), ('delete', 'Delete')], default='view')

    def set_permissions(self, role, document, access_level):
        self.role = role
        self.document = document
        self.access_level = access_level
        self.save()

    def update_permissions(self, role=None, document=None, access_level=None):
        if role:
            self.role = role
        if access_level:
            self.access_level = access_level
        if document:
            self.document = document
        self.save()
        return self

    def remove_permissions(self, role, document):
        permission = DocumentAccessPermission.objects.get(document=document, role=role)
        permission.delete()

    def get_permissions(self):
        return {
            'id': self.id,
            'role': self.role,
            'document': self.document,
            'access_level': self.access_level
        }

class PortfolioDocumentNotification(Notification):
    document = models.ForeignKey(PortfolioDocument, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255, choices=[('expiration', 'Expiration'), ('renewal', 'Renewal')], default='expiration')

    def create_notification(self, message, document, status, date, notification_type):
        PortfolioDocumentNotification.objects.create(message=message, status=status, date=date, document=document, notification_type=notification_type)

    def update_notification(self, message, status, date, document_id, notification_type):
        if message:
            self.message = message
        if status:
            self.status = status
        if date:
            self.date = date
        if document_id:
            self.document.document_id = document_id
        if notification_type:
            self.notification_type = notification_type
        self.save()
        return self

    def delete_notification(self):
        self.delete()

    def get_notifications(self):
        return {
            'id': self.notification_id,
            'message': self.message,
            'status': self.status,
            'date': self.date,
            'document': self.document.document_id,
            'notification_type': self.notification_type
        }

    def list_notifications(cls, filters=None):
        if filters:
            return cls.objects.filter(**filters)
        return cls.objects.all()


class DocumentShare(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(PortfolioDocument, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=255, choices=[('view', 'View'), ('edit', 'Edit'), ('download', 'Download')], default='view')
    shared_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def share_document(self, document, shared_with, access_level):
        DocumentShare.objects.create(document=document, shared_with=shared_with, access_level=access_level)

    def update_share(self, document_id, shared_with, shared_date, access_level):
        if document_id:
            self.document.document_id = document_id
        if shared_with:
            self.status = shared_with
        if access_level:
            self.date = access_level
        if shared_date:
            self.shared_date = shared_date
        self.save()
        return self

    def revoke_share(self, share_id):
        share = DocumentShare.objects.get(id=share_id)
        share.delete()

    def get_shares(self):
        return {
            'id': self.id,
            'document': self.document.document_id,
            'shared_with': self.shared_with.username,
            'access_level': self.access_level,
            'shared_date': self.shared_date
        }

    def list_shares(cls, filters=None):
        if filters:
            return cls.objects.filter(**filters)
        return cls.objects.all()


class AuditLog(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(PortfolioDocument, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, choices=[('view', 'View'), ('download', 'Download'), ('modify', 'Modify')], default='view')
    details = models.TextField(blank=True, null=True)

    def log_action(self, document, user, action_type, details):
        AuditLog.objects.create(document=document, user=user, action_type=action_type, details=details)

    def get_logs(self):
        return {
            'id': self.id,
            'document': self.document.document_id,
            'property_manager': self.property_manager.user_id,
            'action_type': self.action_type,
            'details': self.details
        }

    def list_logs(cls, filters=None):
        if filters:
            return cls.objects.filter(**filters)
        return cls.objects.all()

