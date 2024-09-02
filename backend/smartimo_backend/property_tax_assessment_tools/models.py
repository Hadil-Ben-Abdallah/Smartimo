from django.db import models
from core.models import Document, Resource, Notification, TimeStampedModel
from property_listing.models import PropertyOwner

class PropertyTaxAssessmentTool(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    property_info = models.JSONField(blank=True, null=True) 
    assessed_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    estimated_tax_liability = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    actual_tax_bill = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    discrepancy = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def calculate_estimated_tax(self):
        self.estimated_tax_liability = self.assessed_value * self.tax_rate / 100
        self.save()

    def compare_with_actual_tax(self):
        if self.actual_tax_bill and self.estimated_tax_liability:
            self.discrepancy = self.actual_tax_bill - self.estimated_tax_liability
            self.save()

    def update_property_info(self, new_property_info):
        self.property_info = new_property_info
        self.save()

class PropertyTaxGuidanceResource(Resource):
    RESOURCE_TYPES = [
        ('guide', 'Guide'),
        ('article', 'Article'),
        ('faq', 'FAQ'),
    ]
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='guide')
    external_links = models.JSONField(blank=True, null=True)

    def access_resource(self):
        return {
            'resource_type': self.resource_type,
            'external_links': self.external_links
        }

    def search_resource(self, query):
        if query.lower() in self.resource_type.lower():
            return self.access_resource()
        return None

    def list_related_resources(self, resource_type=None):
        if resource_type:
            return PropertyTaxGuidanceResource.objects.filter(resource_type=resource_type)
        return PropertyTaxGuidanceResource.objects.all()

class TaxAssessmentDocumentManager(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    uploaded_documents = models.ManyToManyField(Document, related_name='tax_documents')
    document_category = models.CharField(max_length=50, blank=True, null=True)
    checklist = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('complete', 'Complete'), ('incomplete', 'Incomplete')], default='incomplete')

    def upload_document(self, document):
        self.uploaded_documents.add(document)
        self.save()

    def categorize_document(self, category):
        self.document_category = category
        self.save()

    def check_document_completeness(self):
        complete = all(item['status'] == 'complete' for item in self.checklist)
        self.status = 'complete' if complete else 'incomplete'
        self.save()

class TaxAssessmentNotification(Notification):
    property_owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=[('deadline', 'Deadline'), ('reminder', 'Reminder'), ('required_action', 'Required Action')])
    link_to_tool = models.URLField(max_length=200, blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True)

    def customize_notification_settings(self, new_preferences):
        self.preferences = new_preferences
        self.save()

    def schedule_reminder(self, reminder_date, action_required):
        return f'Reminder scheduled for {reminder_date} to {action_required}.'

class TaxAppealPreparationTool(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    guidance_content = models.TextField(blank=True, null=True)
    sample_materials = models.JSONField(blank=True, null=True)
    interactive_simulations = models.JSONField(blank=True, null=True)

    def access_guidance_content(self):
        return self.guidance_content

    def download_sample_materials(self):
        return self.sample_materials

    def run_simulation(self, simulation_params):
        return f'Simulation run with parameters: {simulation_params}.'

