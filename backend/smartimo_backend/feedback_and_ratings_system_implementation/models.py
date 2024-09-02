from django.db import models
from core.models import User, Feedback, Report, TimeStampedModel
from lease_rental_management.models import PropertyManager
from property_listing.models import ThePropertyListing
from feedback_and_review_system.models import FeedbackNotification

class SystemImplementationFeedback(Feedback):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property= models.ForeignKey(ThePropertyListing, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    anonymous = models.BooleanField(default=False)

    def submit_feedback(self):
        feedback = SystemImplementationFeedback.objects.create(
            user=self.user,
            property_id=self.property.property_id,
            anonymous=self.anonymous,
            rating=self.rating,
            comments=self.comments
        )
        return feedback

    def view_feedback(self):
        feedback_details = {
            "user": self.user if not self.anonymous else "Anonymous",
            "property": self.property.address,
            "rating": self.rating,
            "comments": self.comments,
            "submitted_at": self.created_at
        }
        return feedback_details

class RatingCriteria(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=100, blank=True, null=True)

    def define_criteria(self, criteria_name):
        new_criteria = RatingCriteria.objects.create(criteria_name=criteria_name)
        return new_criteria

    def modify_criteria(self, criteria_id, new_criteria_name):
        criteria = RatingCriteria.objects.get(id=criteria_id)
        criteria.criteria_name = new_criteria_name
        criteria.save()
        return criteria

    def delete_criteria(self, criteria_id):
        criteria = RatingCriteria.objects.get(id=criteria_id)
        criteria.delete()
        return f"Criteria with ID {criteria_id} has been deleted."

class ImplementationFeedbackNotification(FeedbackNotification):
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    feedback = models.ForeignKey(SystemImplementationFeedback, on_delete=models.CASCADE)

    def notify_manager(self):
        notification_message = f"New feedback received for property {self.feedback.property.address}."
        return notification_message

class FeedbackDashboard(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    feedback_data = models.JSONField(blank=True, null=True)
    analytics = models.JSONField(blank=True, null=True)

    def view_dashboard(self):
        dashboard_data = {
            "feedback_data": self.feedback_data,
            "analytics": self.analytics
        }
        return dashboard_data

    def analyze_feedback(self):
        trends = {
            "positive_feedback": sum(1 for feedback in self.feedback_data if feedback['rating'] > 3),
            "negative_feedback": sum(1 for feedback in self.feedback_data if feedback['rating'] <= 3),
        }
        return trends

    def generate_report(self):
        report = {
            "total_feedback": len(self.feedback_data),
            "average_rating": sum(feedback['rating'] for feedback in self.feedback_data) / len(self.feedback_data)
        }
        return report

class PropertyProfile(TimeStampedModel):
    property = models.ForeignKey(ThePropertyListing, on_delete=models.CASCADE)
    feedback_data = models.JSONField(blank=True, null=True)

    def view_property_feedback(self):
        return self.feedback_data

    def filter_feedback(self, criteria):
        filtered_feedback = [fb for fb in self.feedback_data if fb['criteria'] == criteria]
        return filtered_feedback

    def sort_feedback(self, order):
        sorted_feedback = sorted(self.feedback_data, key=lambda x: x['rating'], reverse=(order == "desc"))
        return sorted_feedback

class FeedbackModerator(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    moderation_logs = models.JSONField(blank=True, null=True)
    reported_issues = models.JSONField(blank=True, null=True)

    def review_feedback(self, feedback_id):
        feedback = SystemImplementationFeedback.objects.get(id=feedback_id)
        return feedback.view_feedback()

    def approve_feedback(self, feedback_id):
        feedback = SystemImplementationFeedback.objects.get(id=feedback_id)
        feedback.is_approved = True
        feedback.save()
        return f"Feedback {feedback_id} approved."

    def reject_feedback(self, feedback_id):
        feedback = SystemImplementationFeedback.objects.get(id=feedback_id)
        feedback.delete()
        return f"Feedback {feedback_id} rejected and deleted."

    def log_moderation_action(self, action):
        self.moderation_logs.append(action)
        self.save()
        return f"Action logged: {action}"

    def resolve_reported_issue(self, issue_id):
        issue = [issue for issue in self.reported_issues if issue['id'] == issue_id]
        if issue:
            self.reported_issues.remove(issue[0])
            self.save()
            return f"Issue {issue_id} resolved."
        return f"Issue {issue_id} not found."

class FeedbackReport(Report):
    feedback = models.ForeignKey(SystemImplementationFeedback, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('sent', 'Sent')], default="pending")

    def submit_report(self):
        report = FeedbackReport.objects.create(
            feedback_id=self.feedback.feedback_id,
            user=self.user.username,
            issue=self.issue,
            status=self.status
        )
        return report

    def view_report(self, report_id):
        report = FeedbackReport.objects.get(id=report_id)
        report_details = {
            "feedback": report.feedback.view_feedback(),
            "issue": report.issue,
            "status": report.status
        }
        return report_details

    def update_report_status(self, report_id, new_status):
        report = FeedbackReport.objects.get(id=report_id)
        report.status = new_status
        report.save()
        return f"Report {report_id} status updated to {new_status}."

class FeedbackAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(ThePropertyListing, on_delete=models.CASCADE)
    summary = models.TextField(blank=True, null=True)
    trend_analysis = models.JSONField(blank=True, null=True)

    def generate_summary(self, property_id):
        feedback_data = SystemImplementationFeedback.objects.filter(id=property_id)
        average_rating = sum(fb.rating for fb in feedback_data) / len(feedback_data)
        self.summary = f"Average Rating: {average_rating}"
        self.save()
        return self.summary

    def identify_trends(self, property_id):
        feedback_data = SystemImplementationFeedback.objects.filter(property=property_id)
        trends = {
            "positive_feedback": sum(1 for fb in feedback_data if fb.rating > 3),
            "negative_feedback": sum(1 for fb in feedback_data if fb.rating <= 3),
        }
        self.trend_analysis = trends
        self.save()
        return trends

    def export_analytics(self, property_id):
        summary = self.generate_summary(property_id)
        trends = self.identify_trends(property_id)
        analytics_data = {
            "summary": summary,
            "trends": trends
        }
        return analytics_data

