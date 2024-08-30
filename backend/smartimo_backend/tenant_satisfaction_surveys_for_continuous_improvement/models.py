from django.db import models
from datetime import datetime, timedelta
from core.models import Property
from maintenance_and_service_requests.models import MaintenancePropertyManager
from lease_rental_management.models import Tenant
from tenant_portal_feedback_submission.models import FeedbackSubmission

class TenantSurveyCreation(models.Model):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(MaintenancePropertyManager, on_delete=models.CASCADE)
    survey_template = models.TextField(blank=True, null=True)
    distribution_schedule = models.DateTimeField(blank=True, null=True)
    trigger_events = models.CharField(max_length=255, blank=True, null=True)

    def create_survey(self, survey_template, distribution_schedule, trigger_events):
        self.survey_template = survey_template
        self.distribution_schedule = distribution_schedule
        self.trigger_events = trigger_events
        self.save()
        return self

    def schedule_distribution(self, interval_days=30):
        next_distribution = self.distribution_schedule + timedelta(days=interval_days)
        self.distribution_schedule = next_distribution
        self.save()
        return f"Survey scheduled for {self.distribution_schedule}"

    def track_response_metrics(self):
        total_surveys = FeedbackSubmission.objects.filter(survey=self).count()
        completed_surveys = FeedbackSubmission.objects.filter(survey=self, responses__isnull=False).count()
        response_rate = (completed_surveys / total_surveys) * 100 if total_surveys > 0 else 0
        return {
            "total_surveys": total_surveys,
            "completed_surveys": completed_surveys,
            "response_rate": response_rate,
        }

class SurveyAnalytics(models.Model):
    survey = models.ForeignKey(TenantSurveyCreation, on_delete=models.CASCADE)
    response_data = models.JSONField(blank=True, null=True)
    analysis_results = models.JSONField(null=True, blank=True)
    trend_data = models.JSONField(null=True, blank=True)

    def analyze_responses(self):
        responses = FeedbackSubmission.objects.filter(survey=self.survey)
        response_list = [response.responses for response in responses]
        self.response_data = response_list
        
        total_score = sum(response.get("satisfaction_score", 0) for response in response_list)
        avg_score = total_score / len(response_list) if response_list else 0
        self.analysis_results = {"average_satisfaction_score": avg_score}
        self.save()
        return self.analysis_results

    def generate_reports(self):
        report = {
            "survey_id": self.survey.id,
            "total_responses": len(self.response_data),
            "average_satisfaction_score": self.analysis_results.get("average_satisfaction_score"),
        }
        return report

    def compare_benchmarks(self, benchmark_data):
        comparison = {
            "current_avg_score": self.analysis_results.get("average_satisfaction_score"),
            "benchmark_avg_score": benchmark_data.get("average_satisfaction_score"),
            "comparison_result": "Above Benchmark" if self.analysis_results.get("average_satisfaction_score") > benchmark_data.get("average_satisfaction_score") else "Below Benchmark"
        }
        return comparison

class TenantFollowUpActions(models.Model):
    id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(TenantSurveyCreation, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    action_description = models.TextField(blank=True, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices= [('pending', 'Pending'), ('overdue', 'Overdue'), ('completed', 'Completed')],default='pending')
    deadline = models.DateTimeField()

    def create_action(self, action_description, assigned_to, deadline):
        self.action_description = action_description
        self.assigned_to = assigned_to
        self.deadline = deadline
        self.save()
        return f"Action created for survey {self.survey} and assigned to {self.assigned_to}."

    def assign_action(self, assignee):
        self.assigned_to = assignee
        self.save()
        return f"Action {self.id} assigned to {self.assigned_to}."

    def track_progress(self):
        if datetime.now() > self.deadline:
            self.status = 'overdue'
        elif self.status == 'completed':
            return f"Action {self.id} is already completed."
        self.save()
        return {"action_id": self.id, "status": self.status}

class TenantSatisfactionMetrics(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100, blank=True, null=True)
    tenant_satisfaction_score = models.FloatField(blank=True, null=True)
    historical_data = models.JSONField(blank=True, null=True)
    performance_indicators = models.JSONField(blank=True, null=True)

    def track_metrics(self, survey_analytics):
        self.tenant_satisfaction_score = survey_analytics.get("average_satisfaction_score")
        self.historical_data.append(self.tenant_satisfaction_score)
        self.save()
        return f"Metrics updated for property {self.id}."

    def analyze_trends(self):
        trend_analysis = {
            "max_score": max(self.historical_data),
            "min_score": min(self.historical_data),
            "avg_score": sum(self.historical_data) / len(self.historical_data),
        }
        return trend_analysis

    def generate_performance_reports(self):
        report = {
            "property_id": self.property.property_id,
            "metric_name": self.metric_name,
            "latest_satisfaction_score": self.tenant_satisfaction_score,
            "historical_data": self.historical_data,
            "trend_analysis": self.analyze_trends(),
        }
        return report

