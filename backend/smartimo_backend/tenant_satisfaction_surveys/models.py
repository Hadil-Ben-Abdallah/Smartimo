from django.db import models
from django.utils import timezone
from core.models import Property, TimeStampedModel
from lease_rental_management.models import Tenant, PropertyManager

class TenantSatisfactionSurvey(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_by = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    survey_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    questions = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    distribution_channels = models.JSONField(blank=True, null=True)
    frequency = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def create_survey(self, title, description, questions, channels, frequency, start_date, end_date):
        self.survey_title = title
        self.description = description
        self.questions = questions
        self.distribution_channels = channels
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.save()

    def edit_survey(self, title=None, description=None, questions=None, channels=None, frequency=None, start_date=None, end_date=None):
        if title:
            self.survey_title = title
        if description:
            self.description = description
        if questions:
            self.questions = questions
        if channels:
            self.distribution_channels = channels
        if frequency:
            self.frequency = frequency
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        self.save()

    def distribute_survey(self):
        pass

    def get_survey_results(self):
        return TenantSurveyResponse.objects.filter(survey=self)

    def activate_survey(self):
        self.is_active = True
        self.save()

    def deactivate_survey(self):
        self.is_active = False
        self.save()


class SurveyQuestion(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(TenantSatisfactionSurvey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, blank=True, null=True)
    question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('rating_scale', 'Rating Scale')], default='multiple_choice')
    options = models.JSONField(blank=True, null=True)

    def create_question(self, question_text, question_type, options=None):
        self.question_text = question_text
        self.question_type = question_type
        if options:
            self.options = options
        self.save()

    def edit_question(self, question_text=None, question_type=None, options=None):
        if question_text:
            self.question_text = question_text
        if question_type:
            self.question_type = question_type
        if options:
            self.options = options
        self.save()

    def get_question(self):
        return self


class TenantSurveyResponse(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    survey = models.ForeignKey(TenantSatisfactionSurvey, on_delete=models.CASCADE)
    responses = models.JSONField(blank=True, null=True)
    submission_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def submit_response(self, survey_id, tenant_id, responses):
        self.survey.id = survey_id
        self.tenant.user_id = tenant_id
        self.responses = responses
        self.save()

    def view_responses(self, survey_id):
        return TenantSurveyResponse.objects.filter(survey=survey_id)

    def analyze_response(self, response_id):
        response = TenantSurveyResponse.objects.get(id=response_id)
        pass


class SurveyResponse(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    response_text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True)

    def create_response(self, question_id, response_text, rating=None):
        self.question.id = question_id
        self.response_text = response_text
        if rating:
            self.rating = rating
        self.save()

    def get_response(self):
        return self


class TenantSurveyAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(TenantSatisfactionSurvey, on_delete=models.CASCADE)
    average_rating = models.FloatField(null=True, blank=True)
    response_count = models.IntegerField(default=0, blank=True, null=True)
    satisfaction_trends = models.JSONField(blank=True, null=True)
    feedback_summary = models.TextField(blank=True, null=True)

    def generate_analytics_report(self):
        return {
            "survey": self.survey.id,
            "average_rating": self.average_rating,
            "response_count": self.response_count,
            "satisfaction_trends": self.satisfaction_trends,
            "feedback-summary": self. feedback_summary
        }

    def analyze_trends(self):
        pass

    def get_feedback_summary(self):
        return self.feedback_summary


class SurveyCollaboration(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    team = models.ManyToManyField(PropertyManager, related_name='collaborations')
    survey = models.ForeignKey(TenantSatisfactionSurvey, on_delete=models.CASCADE)
    discussion_threads = models.JSONField(blank=True, null=True)
    shared_insights = models.JSONField(blank=True, null=True)

    def create_discussion_thread(self, thread_content):
        self.discussion_threads.append(thread_content)
        self.save()

    def share_insights(self, insights):
        self.shared_insights.append(insights)
        self.save()

    def get_collaboration_data(self):
        return {
            "discussion_threads": self.discussion_threads,
            "shared_insights": self.shared_insights
        }

