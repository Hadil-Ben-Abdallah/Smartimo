from django.db import models
from core.models import Property, Category,Feedback, TimeStampedModel
from lease_rental_management.models import PropertyManager, Tenant
from feedback_and_review_system.models import FeedbackNotification
from feedback_and_ratings_system_implementation.models import FeedbackAnalytics, FeedbackDashboard

class StaffMember(Tenant):
    role = models.CharField(max_length=100, choices=[('feedback_manager', 'Feedback Manager'), ('community_liaison', 'Community Liaison')], default='feedback_manager')
    assigned_feedback = models.ManyToManyField(Feedback, blank=True, related_name='assigned_staff')

    def assign_feedback(self, feedback_id):
        feedback = Feedback.objects.get(id=feedback_id)
        self.assigned_feedback.add(feedback)


    def review_feedback(self):
        return self.assigned_feedback.all()

    def send_message_to_tenant(self, tenant_id, message_text):
        tenant = Tenant.objects.get(id=tenant_id)
        message = Message.objects.create(
            recipient=tenant,
            sender=self,
            message_text=message_text
        )
        return message

class Message(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='received_messages')
    sender = models.ForeignKey(StaffMember, on_delete=models.CASCADE, related_name='sent_messages')
    message_text = models.TextField(blank=True, null=True)

class FeedbackSubmission(TimeStampedModel):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('pending_review', 'Pending Review')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority_level = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(StaffMember, on_delete=models.SET_NULL)
    responses = models.JSONField(null=True, blank=True)
    anonymous = models.BooleanField(default=False, blank=True, null=True)
    language_preference = models.CharField(max_length=10, choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French')], default='en')

    def submit_feedback(self, tenant_id, property_id, category, details, staff_member_id, responses, anonymous=False):
        self.tenant.user_id = tenant_id
        self.property.property_id = property_id
        self.category = category
        self.details = details
        self.status = 'open'
        self.priority_level = 'medium'
        self.assigned_to = staff_member_id
        self.responses = responses
        self.anonymous = anonymous
        self.save()

    def update_status(self, submission_id, status):
        feedback_submission = FeedbackSubmission.objects.get(id=submission_id)
        feedback_submission.status = status
        feedback_submission.save()

    def assign_feedback(self, submission_id, staff_member_id):
        feedback_submission = FeedbackSubmission.objects.get(id=submission_id)
        feedback_submission.assigned_to.user_id = staff_member_id
        feedback_submission.save()

    def get_feedback_details(self, submission_id):
        feedback_submission = FeedbackSubmission.objects.get(id=submission_id)
        return {
            'id': feedback_submission.id,
            'tenant': feedback_submission.tenant.username,
            'property': feedback_submission.property.address,
            'category': feedback_submission.category,
            'details': feedback_submission.details,
            'status': feedback_submission.status,
            'priority_level': feedback_submission.priority_level,
            'assigned_to': feedback_submission.assigned_to.username,
            'responses': feedback_submission.responses,
            'anonymous': feedback_submission.anonymous
        }

class PortalFeedbackNotification(FeedbackNotification):
    submission = models.ForeignKey(FeedbackSubmission, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)

    def customize_notification_settings(self, channel, frequency, type):
        self.channel = channel
        self.status = frequency
        self.type = type
        self.save()

class FeedbackCategory(Category):
    submission = models.ForeignKey(FeedbackSubmission, on_delete=models.CASCADE)

    def create_category(self, name, description):
        category = FeedbackCategory(name=name, description=description)
        category.save()
        return category

    def assign_category(self, submission_id, category_id):
        feedback_submission = FeedbackSubmission.objects.get(id=submission_id)
        feedback_category = FeedbackCategory.objects.get(id=category_id)
        feedback_submission.category = feedback_category.name
        feedback_submission.save()

    def list_categories(self):
        return FeedbackCategory.objects.all()

class PortalFeedbackAnalytics(FeedbackAnalytics):
    feedback_data = models.JSONField(blank=True, null=True)
    reports = models.JSONField(blank=True, null=True)

    def aggregate_feedback_data(self, property_id):
        feedback_submissions = FeedbackSubmission.objects.filter(property=property_id)
        aggregated_data = {
            'total_submissions': feedback_submissions.count(),
            'by_status': feedback_submissions.values('status').annotate(count=models.Count('status')),
            'by_priority': feedback_submissions.values('priority_level').annotate(count=models.Count('priority_level')),
        }
        self.feedback_data = aggregated_data
        self.save()

    def perform_sentiment_analysis(self, feedback_data):
        sentiment_scores = {}
        for submission in feedback_data:
            if "good" in submission['details'].lower():
                sentiment_scores[submission['id']] = "Positive"
            else:
                sentiment_scores[submission['id']] = "Negative"
        return sentiment_scores

    def get_analytics_dashboard(self, property_id):
        self.aggregate_feedback_data(property_id)
        sentiment_scores = self.perform_sentiment_analysis(self.feedback_data)
        return {
            'feedback_data': self.feedback_data,
            'sentiment_scores': sentiment_scores
        }

class TenantFeedbackDashboard(FeedbackDashboard):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    feedback_history = models.JSONField(blank=True, null=True)

    def view_feedback_history(self, tenant_id):
        feedback_submissions = FeedbackSubmission.objects.filter(tenant=tenant_id)
        history = []
        for submission in feedback_submissions:
            history.append({
                'submission': submission.id,
                'category': submission.category,
                'details': submission.details,
                'status': submission.status,
                'priority_level': submission.priority_level,
                'assigned_to': submission.assigned_to.username,
            })
        self.feedback_history = history
        self.save()
        return history

    def track_feedback_progress(self, tenant_id, submission_id):
        feedback_submission = FeedbackSubmission.objects.get(tenant_id=tenant_id, id=submission_id)
        return {
            'submission': feedback_submission.id,
            'status': feedback_submission.status,
            'priority_level': feedback_submission.priority_level,
            'assigned_to': feedback_submission.assigned_to.username
        }

    def receive_status_updates(self, tenant_id, submission_id):
        feedback_submission = FeedbackSubmission.objects.get(tenant_id=tenant_id, id=submission_id)
        return {
            'message': f"Status update sent for submission ID {submission_id}",
            'status': feedback_submission.status
        }

