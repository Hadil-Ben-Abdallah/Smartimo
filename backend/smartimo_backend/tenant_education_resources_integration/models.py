from django.db import models
from core.models import Category, Resource, Feedback, TimeStampedModel
from lease_rental_management.models import Tenant, PropertyManager

class TenantEducationalResource(Resource):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    format = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)

    def create_resource(self, category, format, author, title, description, contact_info):
        resource = TenantEducationalResource(
            category=category,
            format=format,
            author=author,
            title=title,
            description=description,
            contact_info=contact_info
        )
        resource.save()
        return resource

    def update_resource(self, format=None, title=None, description=None, contact_info=None):
        if format:
            self.format = format
        if title:
            self.title = title
        if description:
            self.description = description
        if contact_info:
            self.contact_info = contact_info
        self.save()
        return self

    def delete_resource(self):
        self.delete()

    def get_resource_details(self):
        return {
            "format": self.format,
            "author": self.author.username,
            "title": self.title,
            "description": self.description,
            "contact_info": self.contact_info,
        }

class TenantResourceEngagement(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    resource = models.ForeignKey(TenantEducationalResource, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0, blank=True, null=True)
    interaction_time = models.DurationField(default=0, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def track_view(self):
        self.view_count += 1
        self.save()
        return self.view_count

    def track_interaction_time(self, time_spent):
        self.interaction_time += time_spent
        self.save()
        return self.interaction_time

    def submit_feedback(self, feedback_text):
        self.feedback = feedback_text
        self.save()
        return self.feedback

    def get_engagement_details(self):
        return {
            "tenant": self.tenant.username,
            "resource_title": self.resource.title,
            "view_count": self.view_count,
            "interaction_time": self.interaction_time,
            "feedback": self.feedback,
        }

class TenantFeedback(Feedback):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    resource = models.ForeignKey(TenantEducationalResource, on_delete=models.CASCADE)

    def submit_feedback(self, comments):
        self.comments = comments
        self.save()
        return self.comments

    def update_feedback(self, comments):
        self.comments = comments
        self.save()
        return self.comments

    def get_feedback_details(self):
        return {
            "tenant": self.tenant.username,
            "resource_title": self.resource.title,
            "rating": self.rating,
            "comments": self.comments,
        }

class ResourceEngagementAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(TenantEducationalResource, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0, blank=True, null=True)
    average_interaction_time = models.DurationField(default=0, blank=True, null=True)
    feedback_rating = models.FloatField(default=0.0, blank=True, null=True)

    def generate_report(self):
        report = {
            "resource": self.resource.title,
            "view_count": self.view_count,
            "average_interaction_time": self.average_interaction_time,
            "feedback_rating": self.feedback_rating,
        }
        return report

    def track_kpis(self, new_view_count, new_interaction_time, new_feedback_rating):
        total_views = self.view_count + new_view_count
        total_interaction_time = self.average_interaction_time * self.view_count + new_interaction_time
        total_feedback = self.feedback_rating * self.view_count + new_feedback_rating

        self.view_count = total_views
        self.average_interaction_time = total_interaction_time / total_views
        self.feedback_rating = total_feedback / total_views
        self.save()

        return {
            "view_count": self.view_count,
            "average_interaction_time": self.average_interaction_time,
            "feedback_rating": self.feedback_rating,
        }

    def get_analytics_details(self):
        return {
            "resource": self.resource.title,
            "view_count": self.view_count,
            "average_interaction_time": self.average_interaction_time,
            "feedback_rating": self.feedback_rating,
        }

class PromotionalCampaign(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    target_audience = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def create_campaign(self, name, description, target_audience, start_date, end_date):
        campaign = PromotionalCampaign(
            name=name,
            description=description,
            target_audience=target_audience,
            start_date=start_date,
            end_date=end_date
        )
        campaign.save()
        return campaign

    def update_campaign(self, name=None, description=None, target_audience=None, start_date=None, end_date=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if target_audience:
            self.target_audience = target_audience
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        self.save()
        return self

    def delete_campaign(self):
        self.delete()

    def track_campaign_performance(self):
        performance_data = {
            "campaign_name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        return performance_data

    def get_campaign_details(self):
        return {
            "name": self.name,
            "description": self.description,
            "target_audience": self.target_audience,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

