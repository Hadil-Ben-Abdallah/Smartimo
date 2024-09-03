from django.db import models
from core.models import Feedback, TimeStampedModel
import json
from lease_rental_management.models import Tenant, PropertyManager


class CommunityPoll(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    questions = models.JSONField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    visibility = models.CharField(max_length=255, choices=[('all_tenants', 'All Tenants'), ('specific_units', 'Specific Units')], default='specific_units')
    created_by = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)

    def create_poll(self, title, description, questions, start_date, end_date, visibility, created_by):
        self.title = title
        self.description = description
        self.questions = questions
        self.start_date = start_date
        self.end_date = end_date
        self.visibility = visibility
        self.created_by = created_by
        self.save()
        return self

    def update_poll(self, title=None, description=None, questions=None, start_date=None, end_date=None, visibility=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if questions is not None:
            self.questions = questions
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        if visibility:
            self.visibility = visibility
        self.save()
        return self

    def delete_poll(self):
        self.delete()

    def get_poll(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'questions': self.questions,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'visibility': self.visibility,
            'created_by': self.created_by.username
        }

    def list_polls(cls, filters=None):
        if filters:
            return cls.objects.filter(**filters)
        return cls.objects.all()

class PollQuestion(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(CommunityPoll, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, blank=True, null=True)
    question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('rating', 'Rating'), ('rating_scale', 'Rating Scale'), ('open_ended', 'Open Ended')], default='multiple_choice')
    options = models.JSONField(blank=True, null=True)

    def add_question(self, poll_id, question_text, question_type, options):
        self.poll = poll_id
        self.question_text = question_text
        self.question_type = question_type
        self.options = options
        self.save()
        return self

    def update_question(self, question_text=None, question_type=None, options=None):
        if question_text:
            self.question_text = question_text
        if question_type:
            self.question_type = question_type
        if options is not None:
            self.options = options
        self.save()
        return self

    def delete_question(self):
        self.delete()

    def get_question(self):
        return {
            'id': self.id,
            'poll': self.poll.id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': self.options
        }

    def list_questions(cls, poll_id=None):
        if poll_id:
            return cls.objects.filter(poll_id=poll_id)
        return cls.objects.all()

class PollResponse(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(CommunityPoll, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    answers = models.JSONField(blank=True, null=True)

    def submit_response(self, poll_id, tenant, answers):
        self.poll = poll_id
        self.tenant = tenant
        self.answers = answers
        self.save()
        return self

    def update_response(self, answers=None):
        if answers is not None:
            self.answers = answers
        self.save()
        return self

    def delete_response(self):
        self.delete()

    def get_response(self):
        return {
            'id': self.id,
            'poll': self.poll.id,
            'tenant': self.tenant,
            'answers': self.answers,
        }

    def list_responses(cls, poll_id=None):
        if poll_id:
            return cls.objects.filter(poll_id=poll_id)
        return cls.objects.all()

class PollAnalytics(TimeStampedModel):
    poll = models.ForeignKey(CommunityPoll, on_delete=models.CASCADE)
    summary_report = models.JSONField(blank=True, null=True)
    graphical_representation = models.JSONField(blank=True, null=True)

    def generate_report(self):
        responses = PollResponse.objects.filter(poll=self.poll)
        summary = {
            "total_responses": responses.count(),
        }
        self.summary_report = summary
        self.save()
        return self

    def analyze_data(self):
        responses = PollResponse.objects.filter(poll=self.poll)
        insights = {
            "trends": [],
            "patterns": [],
        }
        self.summary_report = insights
        self.save()
        return insights

    def export_data(self):
        return json.dumps(self.summary_report)

class PollDataArchive(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(CommunityPoll, on_delete=models.CASCADE)
    archive_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_archieved = models.BooleanField(default=False, blank=True, null=True)
    access_controls = models.JSONField(blank=True, null=True)

    def archive_data(self):
        self.is_archieved = True

    def retrieve_data(self):
        return {
            'id': self.id,
            'poll': self.poll.id,
            'archive_date': self.archive_date,
            'is_archieved': self.is_archieved,
            'access_controls': self.access_controls,
        }

    def delete_archive(self):
        self.delete()

    def list_archives(cls, filters=None):
        if filters:
            return cls.objects.filter(**filters)
        return cls.objects.all()

class PollFeedback(Feedback):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    poll = models.ForeignKey(CommunityPoll, on_delete=models.CASCADE)

    def submit_feedback(self, rating, comments, tenant_id, poll_id):
        self.rating = rating
        self.comments = comments
        self.tenant.user_id = tenant_id
        self.poll.id = poll_id
        self.save()
        return self

    def update_feedback(self, rating=None, comments=None):
        if rating:
            self.rating = rating
        if comments:
            self.comments = comments
        self.save()
        return self

    def get_feedback(self):
        return {
            'id': self.feedback_id,
            'rating': self.rating,
            'comments': self.comments,
            'tenant': self.tenant.user_id,
            'poll': self.poll.id,
        }

    def list_feedback(cls, poll_id=None):
        if poll_id:
            return cls.objects.filter(poll_id=poll_id)
        return cls.objects.all()

