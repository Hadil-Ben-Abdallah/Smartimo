from django.db import models
from lease_rental_management.models import PropertyManager
from legal_document_templates.models import DocumentTemplateLibrary

class AgreementTemplate(DocumentTemplateLibrary):
    property_type = models.CharField(max_length=255, blank=True, null=True)
    lease_jurisdiction = models.CharField(max_length=255, blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    customizable_fields = models.JSONField(blank=True, null=True)

    def customize_template(self, fields):
        for key, value in fields.items():
            if key in self.customizable_fields:
                self.customizable_fields[key] = value
        self.save()
        return self.customizable_fields

    def select_template(self, property_type, lease_jurisdiction):
        return AgreementTemplate.objects.filter(property_type=property_type, lease_jurisdiction=lease_jurisdiction)


class RentalApplicationTemplate(DocumentTemplateLibrary):
    standard_fields = models.JSONField(blank=True, null=True)
    customizable_fields = models.JSONField(blank=True, null=True)
    digital_submission = models.BooleanField(default=True, blank=True, null=True)

    def customize_template(self, fields):
        for key, value in fields.items():
            if key in self.customizable_fields:
                self.customizable_fields[key] = value
        self.save()
        return self.customizable_fields

    def process_application(self, applicant_data):
        processed_data = {}
        for key in self.standard_fields.keys():
            processed_data[key] = applicant_data.get(key)
        return processed_data


class InspectionReportTemplate(DocumentTemplateLibrary):
    inspection_type = models.CharField(max_length=255, blank=True, null=True)
    condition_fields = models.JSONField(blank=True, null=True)
    maintenance_checklist = models.JSONField(blank=True, null=True)
    media_attachments = models.JSONField(default=dict, blank=True, null=True)

    def generate_template(self, inspection_type):
        return InspectionReportTemplate.objects.filter(inspection_type=inspection_type)

    def attach_media(self, media):
        self.media_attachments.update(media)
        self.save()
        return self.media_attachments


class PropertyRelatedDocumentTemplate(DocumentTemplateLibrary):
    document_type = models.CharField(max_length=255, blank=True, null=True)
    customizable_fields = models.JSONField(blank=True, null=True)
    compliance_status = models.BooleanField(default=True, blank=True, null=True)

    def customize_template(self, fields):
        for key, value in fields.items():
            if key in self.customizable_fields:
                self.customizable_fields[key] = value
        self.save()
        return self.customizable_fields

    def ensure_compliance(self, compliance_guidelines):
        self.compliance_status = True
        self.save()
        return self.compliance_status


class LegalComplianceMonitor(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    template_type = models.CharField(max_length=255, blank=True, null=True)
    compliance_guidelines = models.TextField(blank=True, null=True)
    review_schedule = models.DateTimeField(blank=True, null=True)
    notification_settings = models.JSONField(blank=True, null=True)

    def check_compliance(self, template):
        pass

    def update_template(self, template):
        template.ensure_compliance(self.compliance_guidelines)
        template.save()
        return template

    def send_notifications(self):
        pass

