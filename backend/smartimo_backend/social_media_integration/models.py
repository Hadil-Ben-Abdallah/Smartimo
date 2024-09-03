from django.db import models
from datetime import datetime
from core.models import User, Property, TimeStampedModel
from property_listing.models import RealEstateAgent, ThePropertyListing

class SocialMediaAccount(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=[('facebook', 'Facebook'), ('twitter', 'Twitter') ('linkedin', 'LinkedIn'), ('instagram', 'Instagram')], default='facebook')
    account_name = models.CharField(max_length=100)
    access_token = models.TextField(blank=True, null=True)
    connected_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def connect_account(self, user_id, platform, access_token):
        self.user.user_id= user_id
        self.platform = platform
        self.access_token = access_token
        self.connected_at = datetime.now()
        self.save()
        return self

    def disconnect_account(self, account_id):
        account = SocialMediaAccount.objects.get(account_id=account_id)
        account.delete()
        return f"Account {account_id} disconnected successfully."

    def get_connected_accounts(self, user_id):
        return SocialMediaAccount.objects.filter(user=user_id)

class SocialMediaPropertyListing(ThePropertyListing):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    shared_to_social_media = models.JSONField(default=list, blank=True, null=True)

    def create_listing(self, property_id, agent_id, type, description, photos, videos):
        self.property.property_id = property_id
        self.agent.user_id = agent_id
        self.type = type
        self.description = description
        self.photos = photos
        self.videos = videos
        self.save()
        return self

    def update_listing(self, listing_id, property_id, agent_id, description, photos, videos):
        listing = SocialMediaPropertyListing.objects.get(id=listing_id)
        listing.property.property_id = property_id
        listing.agent.user_id = agent_id
        listing.type = type
        listing.description = description
        listing.photos = photos
        listing.videos = videos
        listing.save()
        return listing

    def share_to_social_media(self, listing_id, platform):
        listing = SocialMediaPropertyListing.objects.get(id=listing_id)
        # Share to social media using the platform's API
        listing.shared_to_social_media.append(platform)
        listing.save()
        return f"Listing {listing_id} shared to {platform}."

    def get_listing(self, listing_id):
        return SocialMediaPropertyListing.objects.get(id=listing_id)

class SocialMediaCampaign(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=[('facebook_ads', 'Facebook Ads'), ('twitter_ads', 'Twitter Ads') ('linkedin_ads', 'LinkedIn Ads'), ('instagram_ads', 'Instagram Ads')], default='facebook')
    target_audience = models.JSONField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active','Active'), ('paused', 'Pause')], default='active')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def create_campaign(self, user_id, platform, target_audience, budget, start_date, end_date):
        self.user.user_id = user_id
        self.platform = platform
        self.target_audience = target_audience
        self.budget = budget
        self.status = 'active'
        self.start_date = start_date
        self.end_date = end_date
        self.save()
        return self

    def update_campaign(self, campaign_id, target_audience, budget, status):
        campaign = SocialMediaCampaign.objects.get(id=campaign_id)
        campaign.target_audience = target_audience
        campaign.budget = budget
        campaign.status = status
        campaign.save()
        return campaign

    def get_campaign(self, campaign_id):
        return SocialMediaCampaign.objects.get(id=campaign_id)

    def track_performance(self, campaign_id):
        campaign = SocialMediaCampaign.objects.get(id=campaign_id)
        # Track performance using the platform's API
        return {"performance": "data"}

class SocialMediaEngagement(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=[('facebook', 'Facebook'), ('twitter', 'Twitter') ('linkedin', 'LinkedIn'), ('instagram', 'Instagram')], default='facebook')
    post_id = models.CharField(max_length=100)
    comments = models.JSONField(default=list, blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)
    shares = models.IntegerField(default=0, blank=True, null=True)
    messages = models.JSONField(default=list, blank=True, null=True)

    def get_engagement_details(self, post_id):
        return SocialMediaEngagement.objects.filter(post_id=post_id)

    def respond_to_comment(self, engagement_id, comment_id, response):
        engagement = SocialMediaEngagement.objects.get(engagement_id=engagement_id)
        return f"Response to comment {comment_id} added."

    def respond_to_message(self, engagement_id, message_id, response):
        engagement = SocialMediaEngagement.objects.get(engagement_id=engagement_id)
        return f"Response to message {message_id} added."

    def schedule_post(self, user_id, platform, post_content, schedule_time):
        return f"Post scheduled on {platform} for {schedule_time}."

class SocialMediaAnalytics(TimeStampedModel):
    analytics_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=[('facebook', 'Facebook'), ('twitter', 'Twitter') ('linkedin', 'LinkedIn'), ('instagram', 'Instagram')], default='facebook')
    engagement_metrics = models.JSONField(default=dict, blank=True, null=True)
    audience_demographics = models.JSONField(default=dict, blank=True, null=True)
    ad_performance = models.JSONField(default=dict, blank=True, null=True)
    conversion_data = models.JSONField(default=dict, blank=True, null=True)

    def track_engagement_metrics(self, user_id, platform):
        return {"engagement_metrics": "data"}

    def analyze_audience_demographics(self, user_id, platform):
        return {"audience_demographics": "data"}

    def track_ad_performance(self, campaign_id):
        return {"ad_performance": "data"}

    def generate_analytics_report(self, user_id, platform):
        return {"analytics_report": "data"}

