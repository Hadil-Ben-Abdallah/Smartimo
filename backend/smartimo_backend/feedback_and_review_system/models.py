from django.db import models
from datetime import timezone
from core.models import User, Notification, Property, Feedback

class UserFeedback(Feedback):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def submit_feedback(self, details):
        Feedback.objects.create(user=self.user, property=self.property, **details)

class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    questions = models.JSONField()
    def create_survey(self, title, description, questions):
        self.title = title
        self.description = description
        self.questions = questions
        self.save()

    def send_survey(self, user_id):
        user = User.objects.get(id=user_id)
        print(f"Survey '{self.title}' sent to user {user.email}")

    def collect_responses(self, survey_id, responses):
        survey = Survey.objects.get(id=survey_id)
        print(f"Collected responses for survey '{survey.title}': {responses}")

    def analyze_responses(self, survey_id):
        survey = Survey.objects.get(id=survey_id)
        print(f"Analyzing responses for survey '{survey.title}'")

class Review(Feedback):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def submit_review(self, rating, comments):
        # Ensure the review is valid before saving
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        self.rating = rating
        self.comments = comments
        self.save()
        print(f"Review submitted: Rating={rating}, Comments={comments}")

    def edit_review(self, rating, comments):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        # Edited only within 24 hours of submission
        if (timezone.now() - self.created_at).total_seconds() > 86400:
            raise ValueError("Review can only be edited within 24 hours of submission.")
        self.rating = rating
        self.comments = comments
        self.save()
        print(f"Review edited: Rating={rating}, Comments={comments}")

    def verify_reviewer(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            # Verify if the user has interacted with the agent or property
            has_interacted = self.user.user_id == user_id
            print(f"Reviewer verification for user {user_id}: {'Verified' if has_interacted else 'Not Verified'}")
            return has_interacted
        except User.DoesNotExist:
            return False

class FeedbackNotification(Notification):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.ForeignKey(UserFeedback, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=[('feedback', 'Feedback'), ('reminder', 'Reminder'), ('survey_invitation', 'Survey Invitation')], default='feedback')
    channel = models.CharField(max_length=255, choices=[('email', 'Email'), ('sms', 'SMS'), ('in_app', 'In_app')], default='email')

    def mark_as_read(self, notification_id):
        notification = FeedbackNotification.objects.get(id=notification_id)
        notification.status = 'read'
        notification.save()
        print(f"Notification {notification_id} marked as read.")

    def get_notifications(self, user_id):
        notifications = FeedbackNotification.objects.filter(user_id=user_id)
        return notifications

class Analytics(models.Model):
    id = models.AutoField(primary_key=True)
    feedback_data = models.JSONField()
    survey_data = models.JSONField()
    review_data = models.JSONField()

    def generate_feedback_report(self, criteria):
        report = {}
        filtered_feedback = [feedback for feedback in self.feedback_data if self._meets_criteria(feedback, criteria)]
        report['total_feedback'] = len(filtered_feedback)
        report['average_rating'] = sum(f['rating'] for f in filtered_feedback) / len(filtered_feedback) if filtered_feedback else 0
        report['comments'] = [f['comments'] for f in filtered_feedback]
        print(f"Feedback Report: {report}")
        return report

    def generate_survey_report(self, criteria):
        report = {}
        filtered_responses = [response for response in self.survey_data if self._meets_criteria(response, criteria)]
        report['total_responses'] = len(filtered_responses)
        report['response_summary'] = self._summarize_responses(filtered_responses)
        print(f"Survey Report: {report}")
        return report

    def generate_review_report(self, criteria):
        report = {}
        filtered_reviews = [review for review in self.review_data if self._meets_criteria(review, criteria)]
        report['total_reviews'] = len(filtered_reviews)
        report['average_rating'] = sum(r['rating'] for r in filtered_reviews) / len(filtered_reviews) if filtered_reviews else 0
        report['reviews'] = [r['comments'] for r in filtered_reviews]
        print(f"Review Report: {report}")
        return report

    def identify_trends(self, data):
        trends = {}
        # we're counting occurrences of specific values
        for entry in data:
            key = entry.get('type')
            if key:
                if key not in trends:
                    trends[key] = 0
                trends[key] += 1
        print(f"Trends Identified: {trends}")
        return trends