from django.db import models
from django.utils import timezone
from tenant_satisfaction_surveys.models import TenantSatisfactionSurvey
from core.models import Communication
from lease_rental_management.models import PropertyManager

class TenantFeedbackAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(default=timezone.now)
    survey = models.ForeignKey(TenantSatisfactionSurvey, on_delete=models.CASCADE)
    trends = models.JSONField(default=dict, blank=True, null=True)
    sentiment_analysis = models.JSONField(default=dict, blank=True, null=True)
    key_insights = models.TextField(blank=True, null=True)

    def generate_report(self, survey_id):
        survey = TenantSatisfactionSurvey.objects.get(id=survey_id)
        feedback = survey.get_survey_results.all()
        self.trends = self.identify_trends(feedback)
        self.sentiment_analysis = self.perform_sentiment_analysis(feedback)
        self.key_insights = self.extract_key_insights(feedback)
        self.save()

    def view_report(self, analytics_id):
        return TenantFeedbackAnalytics.objects.get(id=analytics_id)

    def identify_trends(self, feedback):
        feedback_texts = [fb for fb in feedback]
        trends = {
            "common_themes": self.analyze_common_themes(feedback_texts)
        }
        return trends

    def perform_sentiment_analysis(self):
        pass

    def extract_key_insights(self, feedback):
        trends = self.identify_trends(feedback)
        sentiments = self.perform_sentiment_analysis(feedback)
        return f"Key Insights: {trends}, Sentiment: {sentiments}"

class ImprovementInitiative(models.Model):
    id = models.AutoField(primary_key=True)
    related_survey = models.ForeignKey(TenantSatisfactionSurvey, on_delete=models.CASCADE)
    initiated_by = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=[('maintenance', 'Maintenance'), ('amenities', 'Amenities'), ('communication', 'Communication')], default='maintenance')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('planned', 'Planned'), ('in-progress', 'In Progress'), ('completed', 'Completed')], default='planned')
    metrics = models.JSONField(default=dict, blank=True, null=True)

    def create_initiative(self, related_survey_id, initiated_by_id, category, description):
        return ImprovementInitiative.objects.create(
            related_survey=related_survey_id,
            initiated_by=initiated_by_id,
            category=category,
            description=description,
            status='planned',
            metrics={}
        )

    def update_status(self, initiative_id, status):
        initiative = ImprovementInitiative.objects.get(id=initiative_id)
        initiative.status = status
        initiative.save()

    def track_progress(self, initiative_id, metrics):
        initiative = ImprovementInitiative.objects.get(id=initiative_id)
        initiative.metrics = metrics
        initiative.save()

    def view_initiative(self, initiative_id):
        return ImprovementInitiative.objects.get(id=initiative_id)

class StakeholderCommunication(Communication):
    related_report = models.ForeignKey(TenantFeedbackAnalytics, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    recipients = models.JSONField(default=list, blank=True, null=True)
    is_received = models.BooleanField(default=False, blank=True, null=True)
    is_read = models.BooleanField(default=False, blank=True, null=True)

    def create_communication(self, related_report_id, sent_by_id, recipients, message, date):
        return StakeholderCommunication.objects.create(
            related_report=related_report_id,
            sent_by=sent_by_id,
            recipients=recipients,
            message=message,
            date=date
        )

    def track_communication_status(self, communication_id):
        communication = StakeholderCommunication.objects.get(id=communication_id)
        return {
            self.is_received: True,
            self.is_read: True
        }
