from django.db import models
from django.utils import timezone
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from core.models import Property, Document
from lease_rental_management.models import Tenant, PropertyManager

# Model Definitions
class DocumentTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_type = models.CharField(max_length=255, choices=[('lease_agreement', 'Lease Agreement'), ('eviction_notice', 'Eviction Notice')], default='lease_agreement')
    customizable_fields = models.JSONField(blank=True, null=True)
    template_content = models.TextField(blank=True, null=True)
    version = models.IntegerField(default=1)

    def edit_template(self, content, fields):
        self.template_content = content
        self.customizable_fields = fields
        self.save()

    def update_version(self):
        self.version += 1
        self.save()

    def generate_document(self, data):
        document = self.template_content
        for field, value in data.items():
            document = document.replace(f'{{{{ {field} }}}}', value)
        return document


class DocumentTemplateLibrary(models.Model):
    id = models.AutoField(primary_key=True)
    template_category = models.CharField(max_length=255, choices=[('lease', 'Lease'), ('agreements', 'Agreements'), ('disclosures', 'Disclosures')], default='lease')
    templates = models.ManyToManyField(DocumentTemplate, blank=True, null=True)
    jurisdiction = models.CharField(max_length=255)
    industry_guidelines = models.TextField(blank=True, null=True)

    def get_template_list(self, template_type, jurisdiction):
        return DocumentTemplate.objects.filter(template_type=template_type, jurisdiction=jurisdiction)

    def add_template(self, template):
        self.templates.add(template)
        self.save()

    def remove_template(self, template):
        self.templates.remove(template)
        self.save()

    def search_templates(self, category, jurisdiction):
        return self.templates.filter(template_category=category, jurisdiction=jurisdiction)

    def preview_template(self, template_id):
        template = DocumentTemplate.objects.get(pk=template_id)
        return template.template_content

    def get_guidelines(self):
        return self.industry_guidelines


class LeaseAgreementDocument(Document):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    lease_terms = models.TextField(blank=True, null=True)
    rental_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    document_template = models.ForeignKey(DocumentTemplate, on_delete=models.CASCADE)

    def create_agreement(self, template_data):
        template = self.document_template
        self.lease_terms = template.generate_document(template_data)
        self.save()

    def update_agreement(self, new_terms):
        self.lease_terms = new_terms
        self.save()

    def generate_pdf(self):
        context = {
            'lease_terms': self.lease_terms,
            'rental_rate': self.rental_rate,
        }
        html = render_to_string('lease_agreement_pdf.html', context)
        result = BytesIO()
        pdf = pisa.CreatePDF(html, dest=result)
        return result.getvalue()

    def send_for_signature(self):
        from .models import ElectronicSignature
        signature = ElectronicSignature.objects.create(
            document_id=self.document_id,
            signature_status='pending',
            timestamp=timezone.now()
        )
        return signature


class AgreementTenant(Tenant):
    rental_agreements = models.ManyToManyField(LeaseAgreementDocument, blank=True, null=True)

    def review_agreement(self, document_id):
        document = LeaseAgreementDocument.objects.get(pk=document_id)
        return document.lease_terms

    def request_changes(self, document_id, changes):
        document = LeaseAgreementDocument.objects.get(pk=document_id)
        return f"Changes requested for document {document_id}"

    def sign_agreement(self, document_id):
        from .models import ElectronicSignature
        document = LeaseAgreementDocument.objects.get(pk=document_id)
        signature = ElectronicSignature.objects.create(
            document_id=document_id,
            signer_id=self.id,
            signature_status='pending',
            timestamp=timezone.now()
        )
        return signature


class LegalDocumentPropertyManager(PropertyManager):
    managed_properties = models.ManyToManyField(Property, blank=True, null=True)

    def create_document(self, template_id, data):
        template = DocumentTemplate.objects.get(pk=template_id)
        document = LeaseAgreementDocument.objects.create(
            document_template=template
        )
        document.create_agreement(data)
        return document

    def update_document(self, document_id, updated_terms):
        document = LeaseAgreementDocument.objects.get(pk=document_id)
        document.update_agreement(updated_terms)
        return document

    def notify_updates(self):
        return "Notifications sent for document updates."


class DocumentManagementSystem(models.Model):
    id = models.AutoField(primary_key=True)
    documents = models.ManyToManyField(LeaseAgreementDocument, blank=True, null=True)
    version_control = models.JSONField(blank=True, null=True)
    compliance_updates = models.JSONField(blank=True, null=True)

    def maintain_library(self, template_id):
        template = DocumentTemplate.objects.get(pk=template_id)
        return f"Library updated with template {template_id}"

    def track_compliance(self):
        return "Compliance tracked."

    def audit_trail(self, document_id):
        return f"Audit trail generated for document {document_id}"


class ElectronicSignature(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(LeaseAgreementDocument, on_delete=models.CASCADE)
    signer = models.ForeignKey(AgreementTenant, on_delete=models.CASCADE, null=True, blank=True)
    signature_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def initiate_signature(self):
        return f"Signature request initiated for document {self.document.document_id}"

    def track_signature_status(self):
        return self.signature_status

    def log_signature_activity(self):
        return f"Signature activity logged for document {self.document.document_id}."
