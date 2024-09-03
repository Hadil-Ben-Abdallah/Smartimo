from django.db import models
from core.models import Property, Report, TimeStampedModel
from datetime import datetime
from lease_rental_management.models import Tenant, PropertyManager
import csv
from io import StringIO
from django.http import HttpResponse

class EmailCommunicationLog(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    email_subject = models.CharField(max_length=255, blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    date_sent = models.DateTimeField(blank=True, null=True)
    attachment = models.FileField(upload_to='email_attachments/', null=True, blank=True)

    def log_email(self, tenant, property_manager, subject, body, attachment=None):
        self.tenant = tenant
        self.property_manager = property_manager
        self.email_subject = subject
        self.email_body = body
        self.date_sent = datetime.now()
        if attachment:
            self.attachment = attachment
        self.save()

    def search_email_logs(self, tenant_name=None, property_address=None, date=None):
        logs = EmailCommunicationLog.objects.all()
        if tenant_name:
            logs = logs.filter(tenant_id__name__icontains=tenant_name)
        if property_address:
            logs = logs.filter(tenant_id__address__icontains=property_address)
        if date:
            logs = logs.filter(date_sent__date=date)
        return logs

    def view_email_details(self):
        return {
            "tenant": self.tenant.username,
            "property_manager": self.property_manager.username,
            "subject": self.email_subject,
            "body": self.email_body,
            "date_sent": self.date_sent,
            "attachment": self.attachment.url if self.attachment else None,
        }


class PhoneCallLog(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    call_date = models.DateTimeField(blank=True, null=True)
    call_duration = models.DurationField(blank=True, null=True)
    call_subject = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def log_phone_call(self, tenant, property_manager, duration, subject, notes):
        self.tenant = tenant
        self.property_manager = property_manager
        self.call_date = datetime.now()
        self.call_duration = duration
        self.call_subject = subject
        self.notes = notes
        self.save()

    def view_call_logs(self):
        return {
            "tenant": self.tenant.username,
            "property_manager": self.property_manager.username,
            "call_date": self.call_date,
            "call_duration": self.call_duration,
            "call_subject": self.call_subject,
            "notes": self.notes,
        }

    def search_call_logs(self, tenant_name=None, date=None, call_subject=None):
        logs = PhoneCallLog.objects.all()
        if tenant_name:
            logs = logs.filter(tenant_id__name__icontains=tenant_name)
        if date:
            logs = logs.filter(call_date__date=date)
        if call_subject:
            logs = logs.filter(call_subject__icontains=call_subject)
        return logs


class InPersonInteractionLog(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    interaction_date = models.DateTimeField(blank=True, null=True)
    interaction_subject = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    attachments = models.FileField(upload_to='interaction_attachments/', null=True, blank=True)

    def log_interaction(self, tenant, property_manager, subject, notes, attachments=None):
        self.tenant = tenant
        self.property_manager = property_manager
        self.interaction_date = datetime.now()
        self.interaction_subject = subject
        self.notes = notes
        if attachments:
            self.attachments = attachments
        self.save()

    def view_interaction_logs(self):
        return {
            "tenant": self.tenant.username,
            "property_manager": self.property_manager.username,
            "interaction_date": self.interaction_date,
            "interaction_subject": self.interaction_subject,
            "notes": self.notes,
            "attachments": self.attachments.url if self.attachments else None,
        }

    def attach_documents(self, documents):
        self.attachments = documents
        self.save()


class CommunicationSecurity(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    data_encryption = models.CharField(max_length=255, blank=True, null=True)
    access_control = models.CharField(max_length=255, blank=True, null=True)
    compliance_status = models.CharField(max_length=255, choices=[('gdbr', 'GDPR'), ('ccpa', 'CCPA')], default='gdpr')

    def configure_security_settings(self, encryption, access_control):
        self.data_encryption = encryption
        self.access_control = access_control
        self.save()

    def audit_access(self):
        return f"Audit log for property manager {self.property_manager.username}."

    def validate_compliance(self):
        return f"Compliance status: {self.compliance_status}"


class CommunicationHistoryReport(Report):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    communication_type = models.CharField(max_length=50, choices=[('email', 'Email'), ('phone', 'Phone'), ('in_person', 'In Person')], default='email')
    time_range = models.CharField(max_length=50, blank=True, null=True)

    def generate_report(self):
        logs = []
        if self.communication_type == 'email':
            logs = EmailCommunicationLog.objects.filter(tenant=self.tenant_id, property_manager=self.property_manager.user_id)
        elif self.communication_type == 'phone':
            logs = PhoneCallLog.objects.filter(tenant=self.tenant.user_id, property_manager=self.property_manager.user_id)
        elif self.communication_type == 'in_person':
            logs = InPersonInteractionLog.objects.filter(tenant=self.tenant.user_id, property_manager_id=self.property_manager.user_id)

        report = []
        for log in logs:
            report.append(log.view_email_details() if self.communication_type == 'email' else 
                            log.view_call_logs() if self.communication_type == 'phone' else 
                            log.view_interaction_logs())

        return report

    def export_report(self, format):
        report = self.generate_report()
        if format == 'csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(["Communication Type", "Date", "Subject", "Details"])
            for entry in report:
                writer.writerow([self.communication_type, entry['date_sent'] if self.communication_type == 'email' else entry['call_date'] if self.communication_type == 'phone' else entry['interaction_date'], 
                                    entry['email_subject'] if self.communication_type == 'email' else entry['call_subject'] if self.communication_type == 'phone' else entry['interaction_subject'], 
                                    entry['email_body'] if self.communication_type == 'email' else entry['notes']])
            return HttpResponse(output.getvalue(), content_type='text/csv')

        elif format == 'PDF':
            pass

    def share_report(self, recipients):
        pass

