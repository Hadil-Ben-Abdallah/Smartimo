from django.db import models
from core.models import Property, Document, Notification, TimeStampedModel
from lease_rental_management.models import Tenant, PropertyManager
from data_security_and_compliance_implementation.models import ComplianceAudit

class LeaseDocument(Document):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    metadata = models.JSONField(blank=True, null=True)

    def edit_metadata(self, new_metadata):
        self.metadata = new_metadata
        self.save()

    def get_document_details(self):
        return {
            "title": self.title,
            "document_type": self.document_type,
            "file_path": self.file_path,
            "description": self.description,
            "uploaded_by": self.uploaded_by,
            "version": self.version,
            "property": self.property.property_id,
            "tenant": self.tenant.user_id,
            "metadata": self.metadata,
        }

    def delete_document(self):
        self.delete()

    def get_document_version(self, version_number):
        try:
            return LeaseDocumentRevision.objects.get(document=self, revision_number=version_number)
        except LeaseDocumentRevision.DoesNotExist:
            return None


class LeaseDocumentRevision(TimeStampedModel):
    document = models.ForeignKey(LeaseDocument, on_delete=models.CASCADE)
    revision_number = models.IntegerField(blank=True, null=True)
    revision_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(PropertyManager, on_delete=models.SET_NULL, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    changes_summary = models.TextField(blank=True, null=True)

    def add_revision(self, file_path, changes_summary, uploaded_by):
        self.revision_number += 1
        self.file_path = file_path
        self.changes_summary = changes_summary
        self.uploaded_by = uploaded_by
        self.revision_date = models.DateTimeField(auto_now_add=True)
        self.save()

    def get_revision_details(self):
        return {
            "revision_number": self.revision_number,
            "revision_date": self.revision_date,
            "uploaded_by": self.uploaded_by.username if self.uploaded_by else "Unknown",
            "file_path": self.file_path,
            "changes_summary": self.changes_summary,
        }

    def get_revision_history(self):
        return LeaseDocumentRevision.objects.filter(document=self).order_by('-revision_number')


class TenantDocumentAccess(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    document = models.ForeignKey(LeaseDocument, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)

    def grant_access(self):
        self.access_date = models.DateTimeField(auto_now_add=True)
        self.save()

    def revoke_access(self):
        self.delete()

    def get_access_records(self):
        return TenantDocumentAccess.objects.filter(document=self.document).order_by('-access_date')


class LeaseComplianceAudit(ComplianceAudit):
    document = models.ForeignKey(LeaseDocument, on_delete=models.CASCADE)
    compliance_status = models.CharField(max_length=50, blank=True, null=True)
    audit_summary = models.TextField(blank=True, null=True)

    def conduct_audit(self, compliance_status, audit_summary):
        self.compliance_status = compliance_status
        self.audit_summary = audit_summary
        self.save()

    def get_audit_report(self):
        return {
            "document": self.document.document_id,
            "audit_date": self.audit_date,
            "audit_findings": self.audit_findings,
            "compliance_status": self.compliance_status,
            "audit_summary": self.audit_summary,
        }

    def get_audit_history(self):
        return LeaseComplianceAudit.objects.filter(document=self.document).order_by('-id')


class LeaseDocumentNotification(Notification):
    document = models.ForeignKey(LeaseDocument, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, blank=True, null=True)

    def get_notification_details(self):
        return {
            "message": self.message,
            "status":self.status,
            "date": self.date,
            "document": self.document.document_id,
            "recipient": self.recipient.user_id,
            "notification_type": self.notification_type,
        }

    def get_notification_history(self):
        return LeaseDocumentNotification.objects.filter(document=self.document).order_by('-id')