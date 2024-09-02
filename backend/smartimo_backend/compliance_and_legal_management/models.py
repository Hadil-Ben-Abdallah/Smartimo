from django.db import models
from core.models import Property, TimeStampedModel
from task_calendar_management.models import Event

class RegulationRepository(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=255, blank=True, null=True)
    compliance_category = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)

    def store_regulation(self):
        self.save()
        return self

    def search_regulations(self, location=None, property_type=None, category=None):
        regulations = RegulationRepository.objects.all()
        if location:
            regulations = regulations.filter(location=location)
        if property_type:
            regulations = regulations.filter(property_type=property_type)
        if category:
            regulations = regulations.filter(compliance_category=category)
        return regulations

    def notify_updates(self):
        return f"Notification sent for regulation updates: {self.title}"

class LegalDocumentGenerator(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_content = models.TextField(blank=True, null=True)
    property_details = models.JSONField(blank=True, null=True)
    transaction_details = models.JSONField(blank=True, null=True)
    signatures = models.JSONField(blank=True, null=True)

    def generate_document(self):
        return self.template_content

    def customize_document(self, property_details, transaction_details):
        self.property_details = property_details
        self.transaction_details = transaction_details
        return f"Document customized with property and transaction details."

    def manage_signatures(self, signatures):
        self.signatures = signatures
        self.save()
        return f"Signatures updated for document ID: {self.id}"

class ComplianceCalendar(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reminders = models.JSONField(null=True, blank=True)
    compliance_task = models.CharField(max_length=255, blank=True, null=True)

    def add_event(self, event_id, task):
        self.event = event_id
        self.compliance_task = task
        self.save()
        return f"Event added: {task}"

    def set_reminders(self, reminders):
        self.reminders = reminders
        self.save()
        return f"Reminders set: {reminders}"

    def track_deadlines(self):
        return f"Tracking deadlines for event ID: {self.event}"

class DueDiligenceChecker(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=255, blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    risk_assessment = models.TextField(blank=True, null=True)

    def perform_check(self, check_type):
        self.check_type = check_type
        self.results = f"Results for {check_type} check"
        self.save()
        return f"Due diligence check performed: {check_type}"

    def access_reports(self):
        return {"results": self.results, "risk_assessment": self.risk_assessment}

    def share_findings(self, stakeholders):
        return f"Findings shared with: {', '.join(stakeholders)}"

class FairHousingCompliance(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    training_module = models.TextField(blank=True, null=True)
    checklist = models.JSONField(blank=True, null=True)
    audit_trail = models.JSONField(blank=True, null=True)

    def access_training(self):
        return self.training_module

    def evaluate_compliance(self, property_listing):
        return f"Evaluating compliance for property listing: {property_listing}"

    def generate_report(self):
        report = {
            "checklist": self.checklist,
            "audit_trail": self.audit_trail
        }
        return report

