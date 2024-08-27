from django.db import models
from core.models import Property
from task_calendar_management.models import Event

class RegulationRepository(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=255)
    compliance_category = models.CharField(max_length=255)
    version = models.CharField(max_length=50)

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

class LegalDocumentGenerator(models.Model):
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=255)
    template_content = models.TextField()
    property_details = models.JSONField()
    transaction_details = models.JSONField()
    signatures = models.JSONField()

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

class ComplianceCalendar(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reminders = models.JSONField(null=True, blank=True)
    compliance_task = models.CharField(max_length=255)

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

class DueDiligenceChecker(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=255)
    results = models.TextField()
    risk_assessment = models.TextField()

    def perform_check(self, check_type):
        self.check_type = check_type
        self.results = f"Results for {check_type} check"
        self.save()
        return f"Due diligence check performed: {check_type}"

    def access_reports(self):
        return {"results": self.results, "risk_assessment": self.risk_assessment}

    def share_findings(self, stakeholders):
        return f"Findings shared with: {', '.join(stakeholders)}"

class FairHousingCompliance(models.Model):
    id = models.AutoField(primary_key=True)
    training_module = models.TextField()
    checklist = models.JSONField()
    audit_trail = models.JSONField()

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

