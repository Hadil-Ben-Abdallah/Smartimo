from django.db import models
from core.models import Property, User, TimeStampedModel
from property_listing.models import PropertyOwner


class MarketingCampaign(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    properties = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    target_audience = models.TextField(blank=True, null=True)
    channels = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('draft', 'Draft'), ('launched', 'Launched'), ('completed', 'Completed')], default='draft')

    def create_campaign(self, name, properties, start_date, end_date, budget, target_audience, channels):
        self.name = name
        self.properties = properties
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.target_audience = target_audience
        self.channels = channels
        self.status = 'draft'
        self.save()
        return self

    def update_campaign(self, name=None, properties=None, start_date=None, end_date=None, budget=None, target_audience=None, channels=None):
        if name:
            self.name = name
        if properties:
            self.properties = properties
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        if budget:
            self.budget = budget
        if target_audience:
            self.target_audience = target_audience
        if channels:
            self.channels = channels
        self.save()
        return self

    def launch_campaign(self):
        self.status = 'launched'
        self.save()
        return self

    def get_campaign_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'properties': self.properties,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'budget': self.budget,
            'target_audience': self.target_audience,
            'channels': self.channels,
            'status': self.status,
        }

class CampaignApproval(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    comments = models.TextField(blank=True, null=True)

    def review_campaign(self):
        return {
            'campaign': self.campaign.get_campaign_details(),
            'status': self.status,
            'comments': self.comments,
        }

    def approve_campaign(self):
        self.status = 'Approved'
        self.save()
        return self

    def reject_campaign(self, comments):
        self.status = 'rejected'
        self.comments = comments
        self.save()
        return self

class CampaignTemplate(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, choices=[('social_media', 'Social Media'), ('email', 'Email'), ('flyer', 'Flyer')])
    content = models.TextField(blank=True, null=True)
    assets = models.JSONField(blank=True, null=True)

    def create_template(self, name, template_type, content, assets):
        self.name = name
        self.type = template_type
        self.content = content
        self.assets = assets
        self.save()
        return self

    def get_templates(self):
        return CampaignTemplate.objects.all()

    def apply_template(self, campaign):
        campaign.content = self.content
        campaign.save()
        return campaign

class CampaignPerformance(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE)
    impressions = models.IntegerField(blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    leads_generated = models.IntegerField(blank=True, null=True)
    conversion_rate = models.FloatField(blank=True, null=True)

    def track_performance(self, impressions, clicks, leads_generated, conversion_rate):
        self.impressions = impressions
        self.clicks = clicks
        self.leads_generated = leads_generated
        self.conversion_rate = conversion_rate
        self.save()
        return self

    def generate_report(self):
        return {
            'campaign': self.campaign.get_campaign_details(),
            'impressions': self.impressions,
            'clicks': self.clicks,
            'leads_generated': self.leads_generated,
            'conversion_rate': self.conversion_rate,
        }

    def analyze_trends(self):
        trends = {
            'high_performance': True if self.conversion_rate > 5 else False,
            'click_to_lead_ratio': self.clicks / self.leads_generated if self.leads_generated > 0 else 0,
        }
        return trends

class MarketingTeamCollaboration(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    team_members = models.ManyToManyField(User)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE)
    shared_insights = models.JSONField(blank=True, null=True)
    discussions = models.JSONField(blank=True, null=True)

    def share_insights(self, insights):
        self.shared_insights = insights
        self.save()
        return self

    def start_discussion(self, discussion):
        self.discussions = discussion
        self.save()
        return self

    def archive_collaboration(self):
        archived_data = {
            'team_members': list(self.team_members.all()),
            'shared_insights': self.shared_insights,
            'discussions': self.discussions,
        }
        return archived_data